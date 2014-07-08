# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.core.urlresolvers import reverse_lazy

from cosinnus.forms.group import GroupKwargModelFormMixin
from cosinnus.forms.tagged import get_form
from cosinnus.forms.user import UserKwargModelFormMixin

from cosinnus.forms.select2 import TagSelect2Field

from cosinnus_etherpad.models import Etherpad


class _EtherpadForm(GroupKwargModelFormMixin, UserKwargModelFormMixin,
                    forms.ModelForm):

    tags = TagSelect2Field(required=False, data_url=reverse_lazy('cosinnus:select2:tags'))

    class Meta:
        model = Etherpad
        fields = ('title', 'description', 'tags', 'media_tag')
    
    def __init__(self, *args, **kwargs):
        super(_EtherpadForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            # TODO: Uncomment this to re-enable protecting the title of a pad
            #    self.fields['title'].widget.attrs['readonly'] = True
            preresults = self.instance.tags.values_list('name', 'name').all()
            self.fields['tags'].choices = preresults
            self.fields['tags'].initial = [key for key,val in preresults]#[tag.name for tag in self.instance.tags.all()]
            
            # we need to remove this from the initials, or it overwrites the select2 fields initials
            del self.initial['tags']
            
    # TODO: Uncomment this to re-enable protecting the title of a pad
    # def clean_title(self):
    #    if self.instance.pk:
    #        return self.instance.title
    #    else:
    #        return self.cleaned_data['title']

EtherpadForm = get_form(_EtherpadForm, attachable=False)
