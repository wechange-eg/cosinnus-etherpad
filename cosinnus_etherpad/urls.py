# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url

from cosinnus_etherpad.views import (EtherpadView, EtherpadListView,
    EtherpadCreateView, EtherpadDeleteView, EtherpadUpdateView)


cosinnus_group_patterns = patterns('',
    url(r'^list/$',
        EtherpadListView.as_view(),
        name='list'),

    url(r'^list/(?P<tag>[^/]+)/$',
        EtherpadListView.as_view(),
        name='list-filtered'),

    url(r'^create/$',
        EtherpadCreateView.as_view(),
        name='create'),

    url(r'^pad/(?P<slug>[a-zA-Z0-9\-]+)/$',
        EtherpadView.as_view(),
        name='detail'),

    url(r'^pad/(?P<slug>[a-zA-Z0-9\-]+)/delete/$',
        EtherpadDeleteView.as_view(),
        name='delete'),

    url(r'^pad/(?P<slug>[a-zA-Z0-9\-]+)/update/$',
        EtherpadUpdateView.as_view(),
        name='update'),
)


cosinnus_root_patterns = patterns(None)
urlpatterns = cosinnus_group_patterns + cosinnus_root_patterns
