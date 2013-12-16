# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests
import time

from datetime import datetime, timedelta
from django.core.exceptions import ImproperlyConfigured

from cosinnus_etherpad.conf import settings


class EtherpadClient(object):
    apiKey = settings.COSINNUS_ETHERPAD_API_KEY
    baseUrl = settings.COSINNUS_ETHERPAD_BASE_URL

    def __init__(self):
        if not self.apiKey:
            raise ImproperlyConfigured('Missing configuration of COSINNUS_ETHERPAD_API_KEY')

        if not self.baseUrl:
            raise ImproperlyConfigured('Missing configuration of COSINNUS_ETHERPAD_BASE_URL')

    def _method_url(self, method, version='1.2.7'):
        return '/'.join([self.baseUrl, 'api', version, method])

    def get_or_create_group(self, name):
        params = {'apikey': self.apiKey, 'groupMapper': name}
        url = self._method_url('createGroupIfNotExistsFor')

        response = requests.get(url, params=params)

        # TODO handle errors
        if response.status_code == 200:
            data = response.json()

            return data['data']['groupID']
        else:
            return None

    def get_or_create_user(self, username):
        params = {'apikey': self.apiKey, 'authorMapper': username}
        url = self._method_url('createAuthorIfNotExistsFor')

        response = requests.get(url, params=params)

        # TODO handle errors
        if response.status_code == 200:
            data = response.json()

            return data['data']['authorID']
        else:
            return None

    def delete_group(self, name):
        pass

    def create_pad(self, title, group):
        group_id = self.get_or_create_group(group)

        url = self._method_url('createGroupPad')
        params = {'apikey': self.apiKey,
                  'groupID': group_id,
                  'padName': title}

        response = requests.get(url, params=params)

        # TODO handle errors
        if response.status_code == 200:
            data = response.json()

            return data['data']['padID']
        else:
            return None

    def delete_pad(self, pad_id):
        url = self._method_url('deletePad')
        params = {'apikey': self.apiKey, 'padID': pad_id}
        response = requests.get(url, params=params)

        # TODO handle errors
        if response.status_code == 200:
            return True
        else:
            return False

    def create_session(self, group_id, user_id):
        one_year_from_now = datetime.now() + timedelta(days=365)
        valid_until = time.mktime(one_year_from_now.timetuple())

        url = self._method_url('createSession')
        params = {'apikey': self.apiKey,
                  'groupID': group_id,
                  'authorID': user_id,
                  'validUntil': valid_until}

        response = requests.get(url, params=params)

        # TODO handle errors
        if response.status_code == 200:
            data = response.json()

            return data['data']['sessionID']
        else:
            return None
