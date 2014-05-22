
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from haystack import indexes

from cosinnus.utils.search import BaseTaggableObjectIndex

from cosinnus_etherpad.models import Etherpad


class EtherpadIndex(BaseTaggableObjectIndex, indexes.Indexable):
    description = indexes.CharField(model_attr='description')
    pad_id = indexes.CharField(model_attr='pad_id', indexed=False)

    def get_model(self):
        return Etherpad
