# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from cosinnus.authentication.forms import GroupKwargModelFormMixin
from cosinnus.utils.forms import BootstrapTagWidget

from cosinnus_etherpad.models import Etherpad


class EtherpadForm(GroupKwargModelFormMixin, forms.ModelForm):
    class Meta:
        model = Etherpad
        fields = ('title', 'tags')
        widgets = {
            'tags': BootstrapTagWidget(),
        }

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
