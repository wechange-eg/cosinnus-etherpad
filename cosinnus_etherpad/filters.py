'''
Created on 05.08.2014

@author: Sascha
'''
from cosinnus.views.mixins.filters import CosinnusFilterSet
from cosinnus.forms.filters import AllObjectsFilter, DropdownChoiceWidget,\
    SelectUserWidget
import django_filters
from cosinnus_etherpad.models import Etherpad

class EtherpadFilter(CosinnusFilterSet):
    #title = django_filters.CharFilter(label=_('Description'))
    creator = AllObjectsFilter(label=_('Creator'), widget=SelectUserWidget)
    created = django_filters.DateRangeFilter(label=_('Date created'), widget=DropdownChoiceWidget)
    
    class Meta:
        model = Etherpad
        fields = ['creator', 'created'] #creator__username #'title', 
        order_by = ['-created', 'title']
    
    def get_order_by(self, order_value):
        return super(EtherpadFilter, self).get_order_by(order_value)