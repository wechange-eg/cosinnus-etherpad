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

from cosinnus.models import BaseHierarchicalTaggableObjectModel

from etherpad_lite import EtherpadLiteClient, EtherpadException
from cosinnus_etherpad.conf import settings
from cosinnus_etherpad.managers import EtherpadManager
from django.utils.encoding import smart_text
from cosinnus.utils.permissions import filter_tagged_object_queryset_for_user,\
    check_ug_membership
from cosinnus.utils.urls import group_aware_reverse
from django.core.exceptions import ImproperlyConfigured
from cosinnus_etherpad import cosinnus_notifications
from django.contrib.auth import get_user_model
from cosinnus.models.tagged import BaseTagObject
from cosinnus.models.group import CosinnusPortal
from cosinnus.utils.group import get_cosinnus_group_model


def _init_client():
    """Initialises the etherpad lite client"""
    if not hasattr(settings, 'COSINNUS_ETHERPAD_BASE_URL'):
        raise ImproperlyConfigured("You have not configured ``settings.COSINNUS_ETHERPAD_BASE_URL!``")
    return EtherpadLiteClient(
        base_url=settings.COSINNUS_ETHERPAD_BASE_URL,
        api_version='1.2.7',
        base_params={'apikey': settings.COSINNUS_ETHERPAD_API_KEY})


class Etherpad(BaseHierarchicalTaggableObjectModel):

    SORT_FIELDS_ALIASES = [('title', 'title')]

    pad_id = models.CharField(max_length=255, editable=True)
    description = models.TextField(_('Description'), blank=True)
    # a group mapping that corresponds to the etherpads group slug at its creation time
    # used for session creation, and works even after the etherpad group's slug has changed
    group_mapper = models.CharField(max_length=255, editable=True, null=True, blank=True)

    objects = EtherpadManager()

    class Meta(BaseHierarchicalTaggableObjectModel.Meta):
        verbose_name = _('Etherpad')
        verbose_name_plural = _('Etherpads')

    def __init__(self, *args, **kwargs):
        super(Etherpad, self).__init__(*args, **kwargs)
        self.client = _init_client()

    def get_absolute_url(self):
        kwargs = {'group': self.group, 'slug': self.slug}
        return group_aware_reverse('cosinnus:etherpad:pad-detail', kwargs=kwargs)
    
    def get_delete_url(self):
        kwargs = {'group': self.group, 'slug': self.slug}
        return group_aware_reverse('cosinnus:etherpad:pad-delete', kwargs=kwargs)
    
    def get_pad_url(self):
        if self.pk:
            pad_id = quote_plus(self.pad_id.encode('utf8'))
            base_url = self.client.base_url
            base_url = base_url[:base_url.rfind('/api')]
            return '/'.join([base_url, 'p', pad_id])
        return None
    
    def save(self, *args, **kwargs):
        created = bool(self.pk) == False
        super(Etherpad, self).save(*args, **kwargs)
        if created and not self.is_container:
            # todo was created
            cosinnus_notifications.etherpad_created.send(sender=self, user=self.creator, obj=self, audience=get_user_model().objects.filter(id__in=self.group.members).exclude(id=self.creator.pk))
        

    def get_user_session_id(self, user):
        group_mapper = getattr(self, 'group_mapper', None)
        if not group_mapper:
            group_mapper = _get_group_mapping(self.group)
            self.group_mapper = group_mapper
            self.save()
        author_id = self.client.createAuthorIfNotExistsFor(
            authorMapper=user.username)
        group_id = self.client.createGroupIfNotExistsFor(
            groupMapper=group_mapper)
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
    
    def grant_extra_read_permissions(self, user):
        """ Group members may read etherpads if they are not private """
        is_private = False
        if self.media_tag:
            is_private = self.media_tag.visibility == BaseTagObject.VISIBILITY_USER
        return check_ug_membership(user, self.group) and not is_private
    
    def grant_extra_write_permissions(self, user, **kwargs):
        """ Group members may write/delete etherpads if they are not private """
        is_private = False
        if self.media_tag:
            is_private = self.media_tag.visibility == BaseTagObject.VISIBILITY_USER
        return check_ug_membership(user, self.group) and not is_private
    
    def reinit_pad(self):
        old_pad_id = self.pad_id
        group_id = self.client.createGroupIfNotExistsFor(
            groupMapper=_get_group_mapping(self.group))
        
        counter = 0
        while counter < 10:
            counter += 1
            try:
                pad_id = self.client.createGroupPad(
                    groupID=group_id['groupID'],
                    padName=self.slug+'_reinit%d' % counter)
                break
            except EtherpadException:
                pass
            
        self.pad_id = pad_id['padID']
        
        text = self.client.getText(padID=old_pad_id)
        self.client.setText(padID=self.pad_id, text=text['text'])
        
        self.save()
        
        
    def __str__(self):
        return '<Etherpad%s id: %d>' % (' Folder' if self.is_container else '', self.id)
    
    

def _get_group_mapping(group):
    return smart_text('p_%d_g_%s' % (CosinnusPortal.get_current().id, group.slug)).encode('utf-8')


import django
if django.VERSION[:2] < (1, 7):
    from cosinnus_etherpad import cosinnus_app
    cosinnus_app.register()
