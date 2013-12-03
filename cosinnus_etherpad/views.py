# -*- coding: utf-8 -*-
from __future__ import unicode_literals

try:
    from urllib import parse as urlparse
except ImportError:
    from urlparse import urlparse
import logging

from django.core.urlresolvers import reverse
from django.views.generic import DetailView, RedirectView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from extra_views.contrib.mixins import SortableListMixin

from cosinnus.views.mixins.group import (RequireGroupMixin, FilterGroupMixin,
    GroupFormKwargsMixin)
from cosinnus.views.mixins.tagged import TaggedListMixin

from cosinnus_etherpad.conf import settings
from cosinnus_etherpad.models import Etherpad
from cosinnus_etherpad.forms import EtherpadForm


class EtherpadIndexView(RequireGroupMixin, RedirectView):

    def get_redirect_url(self, **kwargs):
        return reverse('cosinnus:etherpad:list',
                       kwargs={'group': self.group.slug})


class EtherpadView(RequireGroupMixin, FilterGroupMixin, DetailView):
    model = Etherpad

    def _get_cookie_domain(self):
        domain = urlparse(settings.COSINNUS_ETHERPAD_BASE_URL).netloc

        # strip the port (if exists)
        domain = domain.split(':')[0]

        # strip the hostname
        split_domain = domain.split('.')
        # only if we have at least 2 dots use the split domain
        # http://curl.haxx.se/rfc/cookie_spec.html
        if len(split_domain) > 2:
            domain = '.' + '.'.join(split_domain[1:])
        else:
            domain = None
        return domain


    def render_to_response(self, context, **response_kwargs):
        response = super(EtherpadView, self).render_to_response(
            context, **response_kwargs)

        # set cross-domain session cookie for etherpad app
        etherpad = context['etherpad']
        user_session_id = etherpad.get_user_session_id(self.request.user)
        domain = self._get_cookie_domain()
        if domain:
            server_name = self.request.META['SERVER_NAME']
            if domain not in server_name:
                logging.warning('SERVER_NAME %s and cookie domain %s don\'t match. Setting a third-party cookie might not work!' % (server_name, domain))
        response.set_cookie('sessionID', user_session_id, domain=domain)

        return response


class EtherpadListView(RequireGroupMixin, FilterGroupMixin, TaggedListMixin,
                       SortableListMixin, ListView):
    model = Etherpad

    def get(self, request, *args, **kwargs):
        self.sort_fields_aliases = self.model.SORT_FIELDS_ALIASES
        return super(EtherpadListView, self).get(request, *args, **kwargs)


class EtherpadAddView(RequireGroupMixin, FilterGroupMixin,
                         GroupFormKwargsMixin, CreateView):
    form_class = EtherpadForm
    model = Etherpad

    def get_context_data(self, **kwargs):
        context = super(EtherpadAddView, self).get_context_data(**kwargs)
        tags = Etherpad.objects.tags()
        context.update({
            'tags': tags
        })
        return context

    def form_valid(self, form):
        self.etherpad = form.save(commit=False)
        self.etherpad.group = self.group
        self.etherpad.save()
        ret = super(EtherpadAddView, self).form_valid(form)
        form.save_m2m()
        return ret


class EtherpadDeleteView(RequireGroupMixin, FilterGroupMixin, DeleteView):
    model = Etherpad

    def get_success_url(self):
        kwargs = { 'group': self.group.slug }
        return reverse('cosinnus:etherpad:list', kwargs=kwargs)


class EtherpadEditView(RequireGroupMixin, FilterGroupMixin,
                         GroupFormKwargsMixin, UpdateView):
    form_class = EtherpadForm
    form_view = 'edit'
    model = Etherpad

    def get_context_data(self, **kwargs):
        context = super(EtherpadEditView, self).get_context_data(**kwargs)
        tags = Etherpad.objects.tags()
        context.update({
            'form_view': self.form_view,
            'tags': tags
        })
        return context
