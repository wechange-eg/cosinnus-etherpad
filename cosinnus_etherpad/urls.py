# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url

from cosinnus_etherpad.views import (
    EtherpadIndexView, EtherpadView, EtherpadListView,
    EtherpadAddView, EtherpadDeleteView, EtherpadEditView)


cosinnus_group_patterns = patterns('',
    url(r'^$',
        EtherpadIndexView.as_view(),
        name='index'),

    url(r'^list/$',
        EtherpadListView.as_view(),
        name='list'),

    url(r'^list/(?P<tag>[^/]+)/$',
        EtherpadListView.as_view(),
        name='list-filtered'),

    url(r'^add/$',
        EtherpadAddView.as_view(),
        name='add'),

    url(r'^(?P<slug>[a-zA-Z0-9\-]+)/$',
        EtherpadView.as_view(),
        name='detail'),

    url(r'^(?P<slug>[a-zA-Z0-9\-]+)/delete/$',
        EtherpadDeleteView.as_view(),
        name='delete'),

    url(r'^(?P<slug>[a-zA-Z0-9\-]+)/edit/$',
        EtherpadEditView.as_view(),
        name='edit'),
)


cosinnus_root_patterns = patterns(None)
urlpatterns = cosinnus_group_patterns + cosinnus_root_patterns
