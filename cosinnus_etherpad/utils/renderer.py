# -*- coding: utf-8 -*-
"""
Created on 08.07.2014

@author: Sascha Narr
"""
from __future__ import unicode_literals

from cosinnus.utils.renderer import BaseRenderer
from cosinnus_etherpad.models import Etherpad
from cosinnus_etherpad.views import list_view
from cosinnus.views.mixins.hierarchy import HierarchicalListCreateViewMixin
from django.shortcuts import render


class EtherpadRenderer(HierarchicalListCreateViewMixin, BaseRenderer):
    
    model = Etherpad
    
    template = 'cosinnus_etherpad/attached_etherpads.html'
    template_single = 'cosinnus_etherpad/single_etherpad.html'
    template_list = 'cosinnus_etherpad/etherpad_list_standalone.html'
    
    @classmethod
    def render(cls, context, myobjs):
        return super(EtherpadRenderer, cls).render(context, etherpads=myobjs)
    
    @classmethod
    def render_list_for_user(cls, user, request, qs_filter={}, limit=30, **kwargs):
        """ Will render a standalone list of items of the renderer's model for
            a user and a request (important if there are forms in the template).
            This function will filter for access permissions for all of the items,
            but any further filtering (group, organization, etc) will have to be
            passed via the qs_filter dict.
        """
        renderer = EtherpadRenderer()
        renderer.object_list = cls.get_object_list_for_user(user, qs_filter, limit=1000000)
        renderer.kwargs = {}
        context = HierarchicalListCreateViewMixin.get_context_data(renderer)
        context.update(kwargs)
        context['object_list'] = context['object_list'][:limit]
        context['objects'] = context['objects'][:limit]
        
        return render(request, cls.get_template_list(), context).content