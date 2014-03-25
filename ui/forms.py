#  ui/forms.py: Forms handlers for the web site
#
#  Copyright 2014 Sudaraka Wijesinghe <sudaraka.org/contact>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

""" Forms handlers for the web site """

from django import forms
from django.db import models

#from data.models.inventory import Item


class Mock(models.Model):
    """ mock """

    name = models.CharField(max_length=32, blank=False, null=False)
    unit_symbol = models.CharField(max_length=8, blank=True)
    unit_weight = models.DecimalField(max_digits=6, decimal_places=2,
                                      default=1)
    purchase_threshold = models.IntegerField(default=21)
    extended_threshold = models.IntegerField(null=True, blank=True)
    heavy = models.BooleanField()


class ItemForm(forms.models.ModelForm):
    """ Form for add/edit items """

    class Meta:  # pylint: disable=I0011,C1001
        """ Meta class for add/edit form """

        model = Mock
        labels = {
            'unit_weight': 'Weight per Unit',
            'unit_symbol': 'Unit Symbol',
            'purchase_threshold': 'Purchase Threshold',
            'extended_threshold': 'Threshold Extend',
            'heavy': 'This is a heavy item'
        }
        widgets = {
            'name': forms.fields.TextInput(attrs={
                'required': 'required',
            }),
            'unit_weight': forms.fields.TextInput(attrs={
                'maxlength': 7,
            }),
        }
