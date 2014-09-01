'''
Created on 05.08.2014

@author: Sascha
'''
from django.utils.translation import ugettext_lazy as _

from cosinnus.views.mixins.filters import CosinnusFilterSet
from cosinnus.forms.filters import AllObjectsFilter, SelectCreatorWidget
from cosinnus_etherpad.models import Etherpad


class EtherpadFilter(CosinnusFilterSet):
    creator = AllObjectsFilter(label=_('Created By'), widget=SelectCreatorWidget)
    
    class Meta:
        model = Etherpad
        fields = ['creator']
        order_by = (
            ('-created', _('Newest Pads')),
            ('title', _('Title')),
        )
    
    def get_order_by(self, order_value):
        return super(EtherpadFilter, self).get_order_by(order_value)
    