# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from extra_views.contrib.mixins import SortableListMixin

from cosinnus.views.mixins.group import (RequireGroupMixin, FilterGroupMixin,
    GroupFormKwargsMixin)
from cosinnus.views.mixins.tagged import TaggedListMixin

from cosinnus_etherpad.models import Etherpad
from cosinnus_etherpad.forms import EtherpadForm


class EtherpadView(RequireGroupMixin, FilterGroupMixin, DetailView):
    model = Etherpad

    def render_to_response(self, context, **response_kwargs):
        response = super(EtherpadView, self).render_to_response(
            context, **response_kwargs)

        etherpad = context['etherpad']
        user_session_id = etherpad.get_user_session_id(self.request.user)
        # set cross-domain session cookie for etherpad app
        response.set_cookie('sessionID', user_session_id,
                            domain='.ideenhochdrei.org')

        return response


class EtherpadListView(RequireGroupMixin, FilterGroupMixin, TaggedListMixin,
                       SortableListMixin, ListView):
    model = Etherpad

    def get(self, request, *args, **kwargs):
        self.sort_fields_aliases = self.model.SORT_FIELDS_ALIASES
        return super(EtherpadListView, self).get(request, *args, **kwargs)


class EtherpadCreateView(RequireGroupMixin, FilterGroupMixin,
                         GroupFormKwargsMixin, CreateView):
    form_class = EtherpadForm
    model = Etherpad

    def get_context_data(self, **kwargs):
        context = super(EtherpadCreateView, self).get_context_data(**kwargs)
        tags = Etherpad.objects.tags()
        context.update({
            'tags': tags
        })
        return context

    def form_valid(self, form):
        self.etherpad = form.save(commit=False)
        self.etherpad.group = self.group
        self.etherpad.save()
        ret = super(EtherpadCreateView, self).form_valid(form)
        form.save_m2m()
        return ret


class EtherpadDeleteView(RequireGroupMixin, FilterGroupMixin, DeleteView):
    model = Etherpad

    def get_success_url(self):
        return reverse('etherpad-list', kwargs={'group': self.group.pk})


class EtherpadUpdateView(RequireGroupMixin, FilterGroupMixin,
                         GroupFormKwargsMixin, UpdateView):
    form_class = EtherpadForm
    form_view = 'update'
    model = Etherpad

    def get_context_data(self, **kwargs):
        context = super(EtherpadUpdateView, self).get_context_data(**kwargs)
        tags = Etherpad.objects.tags()
        context.update({
            'form_view': self.form_view,
            'tags': tags
        })
        return context
