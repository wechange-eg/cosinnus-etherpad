# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from cosinnus.forms.group import GroupKwargModelFormMixin
from cosinnus.forms.tagged import get_form

from cosinnus_etherpad.models import Etherpad


class _EtherpadForm(GroupKwargModelFormMixin, forms.ModelForm):
    class Meta:
        model = Etherpad
        fields = ('title', 'description', 'tags', 'media_tag')

    def __init__(self, *args, **kwargs):
        super(_EtherpadForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['title'].widget.attrs['readonly'] = True

    def clean_title(self):
        if self.instance.pk:
            return self.instance.title
        else:
            return self.cleaned_data['title']


EtherpadForm = get_form(_EtherpadForm, attachable=False)
