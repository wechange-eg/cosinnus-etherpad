# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from cosinnus.forms.group import GroupKwargModelFormMixin
from cosinnus_etherpad.models import Etherpad


class EtherpadForm(GroupKwargModelFormMixin, forms.ModelForm):
    class Meta:
        model = Etherpad
        fields = ('title', 'description', 'tags', 'media_tag')

    def __init__(self, *args, **kwargs):
        super(EtherpadForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['title'].widget.attrs['readonly'] = True

    def clean_title(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.title
        else:
            return self.cleaned_data['title']
