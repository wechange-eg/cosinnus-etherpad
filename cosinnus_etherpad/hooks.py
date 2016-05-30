# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from cosinnus_etherpad.models import _get_group_mapping, _init_etherpad_client, Etherpad, EtherpadException,\
    Ethercalc
from cosinnus.models.group import CosinnusGroup
from cosinnus.conf import settings
from uuid import uuid4

if not getattr(settings, 'COSINNUS_ETHERPAD_DISABLE_HOOKS', False):

    @receiver(post_save, sender=CosinnusGroup)
    def create_etherpad_group(sender, instance, created, **kwargs):
        """
        Receiver to create a group on etherpad server.
        FIXME: Appearently, this receiver is never called...?
        """
        if created:
            client = _init_etherpad_client()
            client.createGroupIfNotExistsFor(groupMapper=_get_group_mapping(instance))
    
    
    """ @receiver(post_delete, sender=CosinnusGroup) """
    """ Disabled the etherpad delete hook, as we now always retain pads on the server for retrieval purposes. """
    def delete_etherpad_group(sender, instance, **kwargs):
        """
        Receiver to delete a group on etherpad server
        """
        if getattr(settings, 'COSINNUS_DELETE_ETHERPADS_ON_SERVER_ON_DELETE', False):
            client = _init_etherpad_client()
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
            
            group_id = instance.client.createGroupIfNotExistsFor(
                groupMapper=groupMapper)
            pad_id = instance.client.createGroupPad(
                groupID=group_id['groupID'],
                padName=instance.slug)
            instance.pad_id = pad_id['padID']
    
    
    
    @receiver(pre_save, sender=Ethercalc)
    def create_ethercalc(sender, instance, **kwargs):
        """
        Receiver to create a new calc on ethercalc server
        """
        if not instance.pk and not instance.is_container:
            groupMapper = _get_group_mapping(instance.group)
            instance.group_mapper = groupMapper
            # we don't actually talk to the server to create a calc; since unknown calcs are
            # created automatically and we have no way of really checking for existing ones with the dumb API
            # we trust uuid4 to create a new pad
            instance.pad_id = groupMapper + '-' + str(uuid4()).replace('-', '')
            
    
    """@receiver(post_delete, sender=Etherpad)"""
    """ Disabled the etherpad delete hook, as we now always retain pads on the server for retrieval purposes. """
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
