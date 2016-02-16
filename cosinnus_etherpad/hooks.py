# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from cosinnus_etherpad.models import _get_group_mapping, _init_client, Etherpad, EtherpadException
from cosinnus.models.group import CosinnusGroup
from cosinnus.conf import settings


@receiver(post_save, sender=CosinnusGroup)
def create_etherpad_group(sender, instance, created, **kwargs):
    """
    Receiver to create a group on etherpad server.
    FIXME: Appearently, this receiver is never called...?
    """
    if created:
        client = _init_client()
        client.createGroupIfNotExistsFor(groupMapper=_get_group_mapping(instance))


@receiver(post_delete, sender=CosinnusGroup)
def delete_etherpad_group(sender, instance, **kwargs):
    """
    Receiver to delete a group on etherpad server
    """
    if getattr(settings, 'COSINNUS_DELETE_ETHERPADS_ON_SERVER_ON_DELETE', False):
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
        groupMapper = _get_group_mapping(instance.group)
        instance.group_mapper = groupMapper
        
        instance.pad_group_slug = instance
        group_id = instance.client.createGroupIfNotExistsFor(
            groupMapper=groupMapper)
        pad_id = instance.client.createGroupPad(
            groupID=group_id['groupID'],
            padName=instance.slug)
        instance.pad_id = pad_id['padID']
        

@receiver(post_delete, sender=Etherpad)
def delete_etherpad(sender, instance, **kwargs):
    """
    Receiver to delete a pad on etherpad server
    """
    if getattr(settings, 'COSINNUS_DELETE_ETHERPADS_ON_SERVER_ON_DELETE', False):
        if not instance.is_container:
            try:
                instance.client.deletePad(padID=instance.pad_id)
            except EtherpadException as exc:
                # failed deletion of missing padIDs is ok
                if 'padID does not exist' not in str(exc):
                    raise
