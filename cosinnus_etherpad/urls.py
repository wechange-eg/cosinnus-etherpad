# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url

from cosinnus_etherpad.views import (EtherpadView, EtherpadListView,
    EtherpadCreateView, EtherpadDeleteView, EtherpadUpdateView)


urlpatterns = patterns('',
    url(r'^list/$',
        EtherpadListView.as_view(),
        name='etherpad-list'),

    url(r'^list/(?P<tag>[^/]+)/$',
        EtherpadListView.as_view(),
        name='etherpad-list-filtered'),

    url(r'^create/$',
        EtherpadCreateView.as_view(),
        name='etherpad-create'),

    url(r'^(?P<slug>[a-zA-Z0-9\-]+)/$',
        EtherpadView.as_view(),
        name='etherpad-detail'),

    url(r'^(?P<slug>[a-zA-Z0-9\-]+)/delete/$',
        EtherpadDeleteView.as_view(),
        name='etherpad-delete'),

    url(r'^(?P<slug>[a-zA-Z0-9\-]+)/update/$',
        EtherpadUpdateView.as_view(),
        name='etherpad-update'),
)
