# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from uuid import uuid4

from cosinnus.models import CosinnusGroup
from cosinnus_etherpad.managers import EtherpadManager
from cosinnus_etherpad.models import Etherpad


class EtherpadManagerTest(TestCase):

    def setUp(self):
        self.group = CosinnusGroup.objects.create(
            name='testgroup-' + str(uuid4()))
        self.pad = Etherpad.objects.create(
            group=self.group, title='testpad')

    def tearDown(self):
        # explicitly need to delete object, otherwise signal post_delete
        # won't be fired and pad on server will persist
        self.pad.delete()

    def test_tags(self):
        tags = ['foo', 'bar']
        for tag in tags:
            self.pad.tags.add(tag)
        manager = EtherpadManager()
        self.assertEqual(manager.tags(), tags)
