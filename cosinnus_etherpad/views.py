# -*- coding: utf-8 -*-
from __future__ import unicode_literals

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
import logging

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView, RedirectView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from extra_views.contrib.mixins import SortableListMixin

from cosinnus.views.export import CSVExportView
from cosinnus.views.mixins.group import (
    RequireReadMixin, RequireWriteMixin, FilterGroupMixin, GroupFormKwargsMixin)
from cosinnus.views.mixins.tagged import TaggedListMixin

from cosinnus_etherpad.conf import settings
from cosinnus_etherpad.models import Etherpad
from cosinnus_etherpad.forms import EtherpadForm

if 'cosinnus_wiki' in settings.INSTALLED_APPS:
    from cosinnus_wiki.models import Page

if 'cosinnus_file' in settings.INSTALLED_APPS:
    from django.core.files.base import ContentFile
    from cosinnus_file.models import FileEntry


class EtherpadIndexView(RequireReadMixin, RedirectView):

    def get_redirect_url(self, **kwargs):
        return reverse('cosinnus:etherpad:list',
                       kwargs={'group': self.group.slug})

index_view = EtherpadIndexView.as_view()


class EtherpadListView(RequireReadMixin, FilterGroupMixin, TaggedListMixin,
                       SortableListMixin, ListView):
    model = Etherpad

    def get(self, request, *args, **kwargs):
        self.sort_fields_aliases = self.model.SORT_FIELDS_ALIASES
        return super(EtherpadListView, self).get(request, *args, **kwargs)

list_view = EtherpadListView.as_view()


class EtherpadDetailView(RequireReadMixin, FilterGroupMixin, DetailView):
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
        if 'cosinnus_wiki' in settings.INSTALLED_APPS:
            context['has_wiki'] = True
        if 'cosinnus_file' in settings.INSTALLED_APPS:
            context['has_file'] = True

        response = super(EtherpadDetailView, self).render_to_response(
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

pad_detail_view = EtherpadDetailView.as_view()


class EtherpadDeleteView(RequireWriteMixin, FilterGroupMixin, DeleteView):
    model = Etherpad

    def get_success_url(self):
        kwargs = {'group': self.group.slug}
        return reverse('cosinnus:etherpad:list', kwargs=kwargs)

pad_delete_view = EtherpadDeleteView.as_view()


class EtherpadFormMixin(
        RequireWriteMixin, FilterGroupMixin, GroupFormKwargsMixin):
    form_class = EtherpadForm
    model = Etherpad

    def get_context_data(self, **kwargs):
        context = super(EtherpadFormMixin, self).get_context_data(**kwargs)
        tags = Etherpad.objects.tags()
        context.update({
            'form_view': self.form_view,
            'tags': tags
        })
        return context


class EtherpadAddView(EtherpadFormMixin, CreateView):
    form_view = 'add'

    def form_valid(self, form):
        self.etherpad = form.save(commit=False)
        self.etherpad.group = self.group
        self.etherpad.save()
        ret = super(EtherpadAddView, self).form_valid(form)
        form.save_m2m()
        return ret

pad_add_view = EtherpadAddView.as_view()


class EtherpadEditView(EtherpadFormMixin, UpdateView):
    form_view = 'edit'

pad_edit_view = EtherpadEditView.as_view()


class EtherpadArchiveMixin(RequireWriteMixin, RedirectView):
    def get_title(self, request, pad_title):
        import time
        from django.utils.timezone import now
#        from django.utils.translation import to_locale
#        import locale
#
#        old_locale = locale.getlocale()
#        lang_code = getattr(request, 'LANGUAGE_CODE', settings.LANGUAGE_CODE)
#        lang_locale = to_locale(settings.LANGUAGE_CODE)
#        locale.setlocale(locale.LC_ALL, str(lang_locale))
#        suffix = ' ' + now().strftime('%c')
#        locale.setlocale(locale.LC_ALL, old_locale)

        suffix = ' ' + str(int(time.mktime(now().timetuple())))
        return settings.COSINNUS_ETHERPAD_PREFIX_TITLE + pad_title + suffix

    def get_redirect_url(self, **kwargs):
        return reverse('cosinnus:etherpad:pad-detail', kwargs={
            'group': self.group.slug,
            'slug': self.kwargs['slug'],
        })


class EtherpadArchiveWikiView(EtherpadArchiveMixin):
    def post(self, request, *args, **kwargs):
        if 'cosinnus_wiki' in settings.INSTALLED_APPS:
            pad = Etherpad.objects.get(slug=kwargs['slug'], group=self.group)
            title = self.get_title(request, pad.title)
            try:
                page = Page.objects.get(title=title, group=self.group)
            except Page.DoesNotExist:
                page = Page(
                    title=title, group=self.group, created_by=request.user)
            page.content = pad.content
            page.save()

            msg = _('Pad has been archived as Wiki page: <a class="alert-link" href="%(href)s">%(title)s</a>') % {
                'href': reverse('cosinnus:wiki:page-detail', kwargs={
                    'group': self.group.slug,
                    'slug': page.slug,
                }),
                'title': title,
            }
            messages.info(request, msg)
        return super(EtherpadArchiveWikiView, self).post(request, *args, **kwargs)

pad_archive_wiki = EtherpadArchiveWikiView.as_view()


class EtherpadArchiveFileView(EtherpadArchiveMixin):
    def _create_folder(self, request, path):
        title = path[1:]

        try:  # don't use get_or_create: uploaded_by doesn't matter for get
            FileEntry.objects.get(title=title, group=self.group, isfolder=True)
        except FileEntry.DoesNotExist:
            FileEntry.objects.create(
                title=title,
                group=self.group,
                isfolder=True,
                uploaded_by=request.user,
                path=path)

    def post(self, request, *args, **kwargs):
        if 'cosinnus_file' in settings.INSTALLED_APPS:
            pad = Etherpad.objects.get(slug=kwargs['slug'], group=self.group)
            title = self.get_title(request, pad.title)
            content = ContentFile(pad.content)
            if settings.COSINNUS_ETHERPAD_FILE_PATH.startswith('/'):
                path = settings.COSINNUS_ETHERPAD_FILE_PATH
            else:
                path = '/' + settings.COSINNUS_ETHERPAD_FILE_PATH

            self._create_folder(request, path)
            try:
                entry = FileEntry.objects.get(title=title, group=self.group)
                entry.file.delete(save=False)
            except FileEntry.DoesNotExist:
                entry = FileEntry(
                    title=title,
                    group=self.group,
                    uploaded_by=request.user,
                    mimetype='text/html',
                    path=path)
                entry.save()  # let slug be calculated
            filename = entry.slug + '.html'
            entry.file.save(filename, content, save=True)

            msg = _('Pad has been archived as File entry: <a class="alert-link" href="%(href)s">%(title)s</a>') % {
                'href': reverse('cosinnus:file:file', kwargs={
                    'group': self.group.slug,
                    'slug': entry.slug,
                }),
                'title': title,
            }
            messages.info(request, msg)
        return super(EtherpadArchiveFileView, self).post(request, *args, **kwargs)

pad_archive_file = EtherpadArchiveFileView.as_view()


class EtherpadExportView(CSVExportView):
    fields = [
        'pad_id',
        'description',
        'content',
    ]
    model = Etherpad
    file_prefix = 'cosinnus_etherpad'

export_view = EtherpadExportView.as_view()
