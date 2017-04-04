# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.core.urlresolvers import reverse_lazy

from cosinnus.forms.group import GroupKwargModelFormMixin
from cosinnus.forms.tagged import get_form
from cosinnus.forms.user import UserKwargModelFormMixin

from cosinnus.forms.select2 import TagSelect2Field

from cosinnus_etherpad.models import Etherpad
from cosinnus.forms.attached_object import FormAttachable


class _EtherpadForm(GroupKwargModelFormMixin, UserKwargModelFormMixin, 
                    FormAttachable):

    class Meta:
        model = Etherpad
        fields = ('title', 'description', 'media_tag')
     
    # TODO: Uncomment this to re-enable protecting the title of a pad
    #def __init__(self, *args, **kwargs):
        #super(_EtherpadForm, self).__init__(*args, **kwargs)
        #if self.instance.pk:
            #    self.fields['title'].widget.attrs['readonly'] = True

    # TODO: Uncomment this to re-enable protecting the title of a pad
    # def clean_title(self):
    #    if self.instance.pk:
    #        return self.instance.title
    #    else:
    #        return self.cleaned_data['title']

EtherpadForm = get_form(_EtherpadForm)
