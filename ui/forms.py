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

import datetime

from django import forms

from data.models.inventory import Item, Purchase


class ItemForm(forms.models.ModelForm):
    """ Form for add/edit items """

    class Meta:  # pylint: disable=I0011,C1001
        """ Meta class for add/edit form """

        model = Item
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
                'class': 'form-control',
            }),
            'unit_symbol': forms.fields.TextInput(attrs={
                'class': 'form-control',
            }),
            'unit_weight': forms.fields.TextInput(attrs={
                'required': 'required',
                'maxlength': 7,
                'type': 'number',
                'class': 'form-control',
            }),
            'purchase_threshold': forms.fields.TextInput(attrs={
                'required': 'required',
                'type': 'number',
                'class': 'form-control',
            }),
            'extended_threshold': forms.fields.TextInput(attrs={
                'type': 'number',
                'class': 'form-control',
            }),
            'heavy': forms.fields.TextInput(attrs={
                'class': 'ull-left',
                'type': 'checkbox',
                'style': 'padding-top: 4px;',
            }),
        }


class PurchaseForm(forms.models.ModelForm):
    """ Form for item purchase """

    class Meta:  # pylint: disable=I0011,C1001
        """ Meta class for item puchase form """

        model = Purchase
        labels = {
            'date': 'Date',
            'quantity': 'Quantity',
        }
        widgets = {
            'item': forms.fields.HiddenInput(),
            'date': forms.fields.DateInput(attrs={
                'required': 'required',
                'class': 'form-control purchase-date',
                'data-date-format': 'yyyy-mm-dd',
                'readonly': 'readonly',
                'value': datetime.date.today().strftime('%Y-%m-%d')
            }),
            'quantity': forms.fields.TextInput(attrs={
                'required': 'required',
                'maxlength': 7,
                'type': 'number',
                'class': 'form-control',
            }),
        }
