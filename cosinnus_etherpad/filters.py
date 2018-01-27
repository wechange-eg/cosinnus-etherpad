'''
Created on 05.08.2014

@author: Sascha
'''
from django.utils.translation import ugettext_lazy as _

from cosinnus.views.mixins.filters import CosinnusFilterSet
from cosinnus.forms.filters import AllObjectsFilter, SelectCreatorWidget,\
    DropdownChoiceWidgetWithEmpty
from cosinnus_etherpad.models import Etherpad
from django_filters.filters import ChoiceFilter
from django.forms import forms


class EtherpadFilter(CosinnusFilterSet):
    creator = AllObjectsFilter(label=_('Created By'), widget=SelectCreatorWidget)
    type = ChoiceFilter(label=_('Type'), choices=((0, _('Etherpad')), (1, _('Ethercalc'))), widget=DropdownChoiceWidgetWithEmpty)
    
    class Meta:
        model = Etherpad
        fields = ['creator', 'type']
        order_by = (
            ('-last_accessed', _('Last accessed')),
            ('-created', _('Newest Pads')),
            ('title', _('Title')),
        )
    
    def get_order_by(self, order_value):
        return super(EtherpadFilter, self).get_order_by(order_value)
    
    