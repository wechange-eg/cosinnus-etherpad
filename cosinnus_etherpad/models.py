# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from six.moves.urllib.parse import quote_plus

import time
from datetime import timedelta
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.utils.timezone import now

from cosinnus.models import BaseTaggableObjectModel, CosinnusGroup

#from cosinnus_etherpad.client import EtherpadClient
from etherpad_lite import EtherpadLiteClient
from cosinnus_etherpad.conf import settings
from cosinnus_etherpad.managers import EtherpadManager


def _init_client():
    """Initialises the etherpad lite client"""
    return EtherpadLiteClient(
        base_url=settings.COSINNUS_ETHERPAD_BASE_URL,
        api_version='1.2.7',
        base_params={'apikey': settings.COSINNUS_ETHERPAD_API_KEY})


class Etherpad(BaseTaggableObjectModel):

    SORT_FIELDS_ALIASES = [('title', 'title')]

    pad_id = models.CharField(max_length=255, editable=False)

    objects = EtherpadManager()

    def __init__(self, *args, **kwargs):
        super(Etherpad, self).__init__(*args, **kwargs)
        self.client = _init_client()

    def get_absolute_url(self):
        kwargs = {'group': self.group.slug, 'slug': self.slug}
        return reverse('cosinnus:etherpad:pad-detail', kwargs=kwargs)

    def get_pad_url(self):
        pad_id = quote_plus(self.pad_id.encode('utf8'))
        return '/'.join([self.client.base_url, 'p', pad_id])

    def get_user_session_id(self, user):
        author_id = self.client.createAuthorIfNotExistsFor(
            authorMapper=user.username)
        group_id = self.client.createGroupIfNotExistsFor(
            groupMapper=self.group.name)
        one_year_from_now = now() + timedelta(days=365)
        valid_until = time.mktime(one_year_from_now.timetuple())

        session_id = self.client.createSession(
            groupID=group_id['groupID'],
            authorID=author_id['authorID'],
            validUntil=valid_until)
        return session_id['sessionID']


@receiver(post_save, sender=CosinnusGroup)
def create_etherpad_group(sender, instance, created, **kwargs):
    """
    Receiver to create a group on etherpad server
    """
    if created:
        client = _init_client()
        client.createGroupIfNotExistsFor(groupMapper=instance.name)


@receiver(post_delete, sender=CosinnusGroup)
def delete_etherpad_group(sender, instance, **kwargs):
    """
    Receiver to delete a group on etherpad server
    """
    client = _init_client()
    group_id = client.createGroupIfNotExistsFor(
        groupMapper=instance.name)
    client.deleteGroup(groupID=group_id['groupID'])


@receiver(pre_save, sender=Etherpad)
def create_etherpad(sender, instance, **kwargs):
    """
    Receiver to create a pad on etherpad server
    """
    if not instance.pk:
        group_id = instance.client.createGroupIfNotExistsFor(
            groupMapper=instance.group.name)
        pad_id = instance.client.createGroupPad(
            groupID=group_id['groupID'],
            padName=instance.slug)
        instance.pad_id = pad_id['padID']


@receiver(post_delete, sender=Etherpad)
def delete_etherpad(sender, instance, **kwargs):
    """
    Receiver to delete a pad on etherpad server
    """
    instance.client.deletePad(padID=instance.pad_id)
