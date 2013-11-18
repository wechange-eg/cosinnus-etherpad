# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from cosinnus.forms.authentication import GroupKwargModelFormMixin

#######################################################################
# This should probably fixed in core - or somewhat removed, as Markus
# mentioned he wanted to get rid of django-bootstraptoolkit
from cosinnus.forms.widgets.bootstrap import BaseBootstrapInputWidget
from taggit.forms import TagWidget
from django.utils.safestring import mark_safe
class BootstrapTagWidget(BaseBootstrapInputWidget, TagWidget):
    append = mark_safe('<i class="icon-tags"></i>')
#######################################################################


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
