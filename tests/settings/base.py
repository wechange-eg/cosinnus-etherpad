# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django

DEBUG = True
TEMPLATE_DEBUG = DEBUG
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
TIME_ZONE = 'Europe/Berlin'
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True
USE_TZ = True
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
SECRET_KEY = 'test-secret-key'
ROOT_URLCONF = 'cosinnus.urls'
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'appconf',
    'bootstrap3',
    'taggit',

    'cosinnus',
    'cosinnus_etherpad',
    'tests',
)
COSINNUS_ETHERPAD_API_KEY = 'z1Y8DmomTWO1NaVV0OKzhUBfnkQdMZGk'
COSINNUS_ETHERPAD_BASE_URL = 'http://pad.sinnwerkstatt.com'
if django.VERSION[:2] < (1, 6):
    TEST_RUNNER = 'discover_runner.DiscoverRunner'
