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
from django.utils.translation import ugettext_lazy as _

from cosinnus.models import BaseHierarchicalTaggableObjectModel, CosinnusGroup

from etherpad_lite import EtherpadLiteClient, EtherpadException
from cosinnus_etherpad.conf import settings
from cosinnus_etherpad.managers import EtherpadManager
from django.utils.encoding import smart_text
from cosinnus.utils.permissions import filter_tagged_object_queryset_for_user
from cosinnus.utils.urls import group_aware_reverse


def _init_client():
    """Initialises the etherpad lite client"""
    return EtherpadLiteClient(
        base_url=settings.COSINNUS_ETHERPAD_BASE_URL,
        api_version='1.2.7',
        base_params={'apikey': settings.COSINNUS_ETHERPAD_API_KEY})


class Etherpad(BaseHierarchicalTaggableObjectModel):

    SORT_FIELDS_ALIASES = [('title', 'title')]

    pad_id = models.CharField(max_length=255, editable=False)
    description = models.TextField(_('Description'), blank=True)

    objects = EtherpadManager()

    class Meta(BaseHierarchicalTaggableObjectModel.Meta):
        verbose_name = _('Etherpad')
        verbose_name_plural = _('Etherpads')

    def __init__(self, *args, **kwargs):
        super(Etherpad, self).__init__(*args, **kwargs)
        self.client = _init_client()

    def get_absolute_url(self):
        kwargs = {'group': self.group.slug, 'slug': self.slug}
        return group_aware_reverse('cosinnus:etherpad:pad-detail', kwargs=kwargs)

    def get_pad_url(self):
        if self.pk:
            pad_id = quote_plus(self.pad_id.encode('utf8'))
            base_url = self.client.base_url
            base_url = base_url[:base_url.rfind('/api')]
            return '/'.join([base_url, 'p', pad_id])
        return None

    def get_user_session_id(self, user):
        author_id = self.client.createAuthorIfNotExistsFor(
            authorMapper=user.username)
        group_id = self.client.createGroupIfNotExistsFor(
            groupMapper=_get_group_mapping(self.group))
        one_year_from_now = now() + timedelta(days=365)
        valid_until = time.mktime(one_year_from_now.timetuple())

        session_id = self.client.createSession(
            groupID=group_id['groupID'],
            authorID=author_id['authorID'],
            validUntil=valid_until)
        return session_id['sessionID']

    @property
    def content(self):
        return self.client.getHTML(padID=self.pad_id)['html']
    
    @classmethod
    def get_current(self, group, user):
        """ Returns a queryset of the current upcoming events """
        qs = Etherpad.objects.filter(group=group)
        if user:
            qs = filter_tagged_object_queryset_for_user(qs, user)
        return qs.filter(is_container=False)
        


@receiver(post_save, sender=CosinnusGroup)
def create_etherpad_group(sender, instance, created, **kwargs):
    """
    Receiver to create a group on etherpad server
    """
    if created:
        client = _init_client()
        client.createGroupIfNotExistsFor(groupMapper=_get_group_mapping(instance))


@receiver(post_delete, sender=CosinnusGroup)
def delete_etherpad_group(sender, instance, **kwargs):
    """
    Receiver to delete a group on etherpad server
    """
    client = _init_client()
    group_id = client.createGroupIfNotExistsFor(
        groupMapper=_get_group_mapping(instance))
    client.deleteGroup(groupID=group_id['groupID'])


@receiver(pre_save, sender=Etherpad)
def create_etherpad(sender, instance, **kwargs):
    """
    Receiver to create a pad on etherpad server
    """
    if not instance.pk and not instance.is_container:
        group_id = instance.client.createGroupIfNotExistsFor(
            groupMapper=_get_group_mapping(instance.group))
        pad_id = instance.client.createGroupPad(
            groupID=group_id['groupID'],
            padName=instance.slug)
        instance.pad_id = pad_id['padID']

@receiver(post_delete, sender=Etherpad)
def delete_etherpad(sender, instance, **kwargs):
    """
    Receiver to delete a pad on etherpad server
    """
    try:
        instance.client.deletePad(padID=instance.pad_id)
    except EtherpadException as exc:
        # failed deletion of missing padIDs is ok
        if 'padID does not exist' not in str(exc):
            raise

def _get_group_mapping(group):
    return smart_text(group.slug).encode('utf-8')


import django
if django.VERSION[:2] < (1, 7):
    from cosinnus_etherpad import cosinnus_app
    cosinnus_app.register()
