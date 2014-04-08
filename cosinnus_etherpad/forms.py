# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from cosinnus.forms.group import GroupKwargModelFormMixin
from cosinnus.forms.tagged import TagObjectFormMixin

from cosinnus_etherpad.models import Etherpad


class EtherpadForm(GroupKwargModelFormMixin, TagObjectFormMixin,
                   forms.ModelForm):
    class Meta:
        model = Etherpad
        fields = ('title', 'description', 'tags', 'media_tag')

    def __init__(self, *args, **kwargs):
        super(EtherpadForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['title'].widget.attrs['readonly'] = True

    def clean_title(self):
        if self.instance.pk:
            return instance.title
        else:
            return self.cleaned_data['title']
