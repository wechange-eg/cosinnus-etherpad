# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def register():
    # Import here to prevent import side effects
    from django.utils.translation import ugettext_lazy as _
    from django.utils.translation import pgettext_lazy

    from cosinnus.core.registries import (app_registry, attached_object_registry, 
        url_registry, widget_registry)

    app_registry.register('cosinnus_etherpad', 'etherpad', _('Etherpads'))   
    attached_object_registry.register('cosinnus_etherpad.Etherpad',
                             'cosinnus_etherpad.utils.renderer.EtherpadRenderer')
    url_registry.register_urlconf('cosinnus_etherpad', 'cosinnus_etherpad.urls')
    widget_registry.register('etherpad', 'cosinnus_etherpad.dashboard.Latest')
    
    # makemessages replacement protection
    name = pgettext_lazy("the_app", "etherpad")
