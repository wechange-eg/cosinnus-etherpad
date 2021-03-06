# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from builtins import str
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from uuid import uuid4

from cosinnus.models import CosinnusGroup
from cosinnus_etherpad.models import Etherpad


class EtherpadTest(TestCase):
    pad_title = 'testpad'

    def setUp(self):
        super(EtherpadTest, self).setUp()
        self.group = CosinnusGroup.objects.create(
            name='testgroup-' + str(uuid4()))
        self.pad = Etherpad.objects.create(
            group=self.group, title=self.pad_title)

    def tearDown(self):
        # explicitly need to delete object, otherwise signals won't be fired
        # and pad/group on server will persist
        self.pad.delete()
        self.group.delete()
        super(EtherpadTest, self).tearDown()

    def test_new_pad(self):
        """
        Should have set title in new pad
        """
        self.assertEqual(self.pad.title, self.pad_title)

    def test_get_pad_url(self):
        """
        Pad URL should contain base URL and pad title
        """
        pad_url = self.pad.get_pad_url()
        # pad URL should contain base URL and pad title
        base_url = settings.COSINNUS_ETHERPAD_BASE_URL
        base_url = base_url[:base_url.rfind('/api')]
        self.assertIn(base_url, pad_url)
        self.assertIn(self.pad_title, pad_url)

    def test_get_user_session_id(self):
        """
        User session id should contain a certain string
        """
        user = User(username='test')
        session_id = self.pad.get_user_session_id(user)
        # session id should start with 's.'
        self.assertIn('s.', session_id)
