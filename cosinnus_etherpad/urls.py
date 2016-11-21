# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url

cosinnus_group_patterns = patterns('cosinnus_etherpad.views',
    url(r'^$', 'index_view', name='index'),
    url(r'^list/$', 'pad_hybrid_list_view', name='list'),
    url(r'^list/move_element/$', 'move_element_view', name='move-element'),
    url(r'^list/(?P<slug>[^/]+)/$', 'pad_hybrid_list_view', name='list'),
    url(r'^(?P<slug>[^/]+)/edit/$', 'pad_write_view', name='pad-write'),
    url(r'^(?P<slug>[^/]+)/settings/$', 'pad_edit_view', name='pad-edit'),
    url(r'^(?P<slug>[^/]+)/$', 'pad_detail_view', name='pad-detail'),
    url(r'^(?P<slug>[^/]+)/csv/$', 'calc_csv_view', name='calc-csv'),
    
    #url(r'^add-container/$', 'container_add_view', name='container-add'),
    url(r'^export/$', 'export_view', name='export'),
    url(r'^(?P<slug>[^/]+)/delete/$', 'pad_delete_view', name='pad-delete'),
    url(r'^(?P<slug>[^/]+)/archive/document/$',
        'pad_archive_document', name='pad-archive-document'),
    url(r'^(?P<slug>[^/]+)/archive/file/$',
        'pad_archive_file', name='pad-archive-file'),
    #url(r'^(?P<slug>[^/]+)/add-container/$',
    #    'container_add_view', name='container-add'),
)


cosinnus_root_patterns = patterns(None)
urlpatterns = cosinnus_group_patterns + cosinnus_root_patterns
