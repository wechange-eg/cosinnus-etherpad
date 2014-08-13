# -*- coding: utf-8 -*-
"""
Created on 08.07.2014

@author: Sascha Narr
"""
from __future__ import unicode_literals

from cosinnus.utils.renderer import BaseRenderer


class EtherpadRenderer(BaseRenderer):

    template = 'cosinnus_etherpad/attached_etherpads.html'
    template_single = 'cosinnus_etherpad/single_etherpad.html'

    @classmethod
    def render(cls, context, myobjs):
        return super(EtherpadRenderer, cls).render(context, etherpads=myobjs)
