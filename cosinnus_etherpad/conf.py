# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from appconf import AppConf


class CosinnusEtherpadConf(AppConf):
    API_KEY = None
    BASE_URL = None