# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from cosinnus_etherpad.models import Etherpad


class EtherpadAdmin(admin.ModelAdmin):
    list_display = ('title', 'group', 'creator', 'path',)
    list_filter = ('group', 'group__portal', 'title')

admin.site.register(Etherpad, EtherpadAdmin)
