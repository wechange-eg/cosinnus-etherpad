# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url

cosinnus_group_patterns = patterns('cosinnus_etherpad.views',
    url(r'^$', 'index_view', name='index'),
    url(r'^list/$', 'list_view', name='list'),
    url(r'^list/(?P<tag>[^/]+)/$', 'list_view', name='list-filtered'),
    url(r'^add/$', 'pad_add_view', name='pad-add'),
    url(r'^export/$', 'export_view', name='export'),
    url(r'^(?P<slug>[a-zA-Z0-9\-]+)/$', 'pad_detail_view', name='pad-detail'),
    url(r'^(?P<slug>[a-zA-Z0-9\-]+)/delete/$', 'pad_delete_view', name='pad-delete'),
    url(r'^(?P<slug>[a-zA-Z0-9\-]+)/edit/$', 'pad_edit_view', name='pad-edit'),
    url(r'^(?P<slug>[a-zA-Z0-9\-]+)/archive/document/$',
        'pad_archive_document', name='pad-archive-document'),
    url(r'^(?P<slug>[a-zA-Z0-9\-]+)/archive/file/$',
        'pad_archive_file', name='pad-archive-file'),
)


cosinnus_root_patterns = patterns(None)
urlpatterns = cosinnus_group_patterns + cosinnus_root_patterns
