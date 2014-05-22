# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def register():
    # Import here to prevent import side effects
    from django.utils.translation import ugettext_lazy as _

    from cosinnus.core.registries import (app_registry, url_registry,
        widget_registry)

    app_registry.register('cosinnus_etherpad', 'etherpad', _('Etherpads'))
    url_registry.register_urlconf('cosinnus_etherpad', 'cosinnus_etherpad.urls')
    widget_registry.register('etherpad', 'cosinnus_etherpad.dashboard.Latest')
