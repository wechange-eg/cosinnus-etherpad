# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url

cosinnus_group_patterns = patterns('cosinnus_etherpad.views',
    url(r'^$', 'index_view', name='index'),
    url(r'^list/$', 'list_view', name='list'),
    url(r'^list/(?P<tag>[^/]+)/$', 'list_view', name='list-filtered'),
    url(r'^add/$', 'add_view', name='add'),
    url(r'^(?P<slug>[a-zA-Z0-9\-]+)/$', 'detail_view', name='detail'),
    url(r'^(?P<slug>[a-zA-Z0-9\-]+)/delete/$', 'delete_view', name='delete'),
    url(r'^(?P<slug>[a-zA-Z0-9\-]+)/edit/$', 'edit_view', name='edit'),
)


cosinnus_root_patterns = patterns(None)
urlpatterns = cosinnus_group_patterns + cosinnus_root_patterns
