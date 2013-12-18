# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from uuid import uuid4

from cosinnus.models import CosinnusGroup
from cosinnus_etherpad.forms import EtherpadForm
from cosinnus_etherpad.models import Etherpad


class EtherpadFormTest(TestCase):

    def setUp(self):
        super(EtherpadFormTest, self).setUp()
        self.group = CosinnusGroup.objects.create(
            name='testgroup-' + str(uuid4()))
        title = 'testpad'
        self.pad = Etherpad.objects.create(
            group=self.group, title=title)
        self.data = {'title': title}

    def tearDown(self):
        # explicitly need to delete object, otherwise signal post_delete
        # won't be fired and pad on server will persist
        self.pad.delete()
        super(EtherpadFormTest, self).tearDown()

    def test_readonly_title(self):
        """
        Should not set the title to readonly in the widget if instance is not
        given
        """
        form = EtherpadForm()
        self.assertNotIn('readonly', form.fields['title'].widget.attrs)

    def test_readonly_title_instance(self):
        """
        Should set the title to readonly in the widget if instance is given
        """
        form = EtherpadForm(instance=self.pad)
        self.assertTrue(form.fields['title'].widget.attrs['readonly'])

    def test_clean_title(self):
        """
        Should clean the title
        """
        form = EtherpadForm(self.data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.clean_title(), form.cleaned_data['title'])

    def test_clean_title_instance(self):
        """
        Should clean the title with instance
        """
        form = EtherpadForm(self.data, instance=self.pad)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.clean_title(), self.pad.title)
