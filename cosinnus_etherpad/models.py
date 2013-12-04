# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from six.moves.urllib.parse import quote_plus

from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.dispatch import receiver

from cosinnus.models import BaseTaggableObjectModel, CosinnusGroup

from cosinnus_etherpad.client import EtherpadClient
from cosinnus_etherpad.managers import EtherpadManager


class Etherpad(BaseTaggableObjectModel):

    SORT_FIELDS_ALIASES = [('title', 'title')]

    def __init__(self, *args, **kwargs):
        super(Etherpad, self).__init__(*args, **kwargs)
        self.client = EtherpadClient()

    pad_id = models.CharField(max_length=255, editable=False)

    objects = EtherpadManager()

    # move to base model?
    class Meta:
        unique_together = (('group', 'slug'),)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        kwargs = {'group': self.group.slug, 'slug': self.slug}
        return reverse('cosinnus:etherpad:pad-detail', kwargs=kwargs)

    def get_pad_url(self):
        pad_id = quote_plus(self.pad_id.encode('utf8'))
        return '/'.join([self.client.baseUrl, 'p', pad_id])

    def get_user_session_id(self, user):
        user_id = self.client.get_or_create_user(user.username)
        group_id = self.client.get_or_create_group(self.group.name)

        return self.client.create_session(group_id, user_id)


@receiver(post_save, sender=CosinnusGroup)
def create_etherpad_group(sender, instance, created, **kwargs):
    if created:
        client = EtherpadClient()
        client.get_or_create_group(instance.name)


@receiver(post_delete, sender=CosinnusGroup)
def delete_etherpad_group(sender, instance, **kwargs):
    pass  # TODO


@receiver(pre_save, sender=Etherpad)
def create_group_etherpad(sender, instance, **kwargs):
    if not instance.pk:
        instance.pad_id = instance.client.create_pad(
            instance.slug, instance.group.name)


@receiver(post_delete, sender=Etherpad)
def delete_group_etherpad(sender, instance, **kwargs):
    pass  # TODO
