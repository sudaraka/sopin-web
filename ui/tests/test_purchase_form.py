#  ui/tests/test_purchase_form.py: Unit tests for item purchase form
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

""" UI Unit test for item purchase form on item maintenance page """

import datetime
import json

from ui.tests.base import BaseUnitTestCase

from ui.forms import PurchaseForm

from data.models.inventory import Item, Purchase


class ItemPurchaseFormTest(BaseUnitTestCase):
    """ Item purchase form unit test """

    uri = '/item-maintenance/purchase/'
    template = 'items/purchase.html'

    def test_uri_render_correct_template(self):
        """ Call base class function """

        self.uri_render_correct_template()

    def test_template_receive_the_form_via_context(self):
        """
        Purchase form template should have the PurchaseForm instance in it's
        context.

        """

        # No item specified
        response = self.client.get(self.uri)

        self.assertIn('form', response.context)
        self.assertEqual(response.context['form'], None)

        self.assertIn('item', response.context)
        self.assertEqual(type(response.context['item']), type(Item()))

        # Non-existing item specified
        response = self.client.get(self.uri + '?item=1')

        self.assertIn('form', response.context)
        self.assertEqual(response.context['form'], None)

        self.assertIn('item', response.context)
        self.assertEqual(type(response.context['item']), type(Item()))

        # Valid item specified
        item = Item.objects.create()
        response = self.client.get(self.uri + '?item=1')

        self.assertIn('form', response.context)
        self.assertEqual(type(response.context['form']), type(PurchaseForm()))

        self.assertIn('item', response.context)
        self.assertEqual(response.context['item'], item)

        # Invalid item specified
        response = self.client.get(self.uri + '?item=-1')

        self.assertIn('form', response.context)
        self.assertEqual(response.context['form'], None)

        self.assertIn('item', response.context)
        self.assertEqual(type(response.context['item']), type(Item()))

    def test_template_receive_the_item_via_context(self):
        """
        Purchase form template should have the current Item object in it's
        context.

        """

        item = Item.objects.create()
        response = self.client.get(self.uri + '?item=1')

        self.assertIn('item', response.context)
        self.assertEqual(response.context['item'], item)

    def test_form_POST_saves_the_new_purchase(self):
        """
        Make sure we can create and save new item purchase by posting the form.

        """

        item = Item.objects.create(name='test item #1')
        self.client.post(self.uri, data={
            'item': str(item.id),
            'quantity': '1',
            'date': datetime.date.today().strftime('%Y-%m-%d'),
        })

        # Verify that we have one item stored
        self.assertEqual(Purchase.objects.count(), 1)

        # Verify the saved item has the same information posted
        saved_purchase = Purchase.objects.first()
        self.assertEqual(saved_purchase.quantity, 1)
        self.assertEqual(saved_purchase.date, datetime.date.today())
        self.assertEqual(saved_purchase.item, item)

    def test_item_data_POST_return_JSON_response(self):
        """ Test if POSTing data to item form returns a valid JSON reponse """

        item = Item.objects.create(name='test item #1')
        response = self.client.post(self.uri, data={
            'item': str(item.id),
            'quantity': '1',
            'date': datetime.date.today().strftime('%Y-%m-%d'),
        })

        self.assertIn('application/json', response['Content-Type'])

        expected_response = {
            'code': 0,
            'message': 'success',
        }

        self.assertEqual(bytes(json.dumps(expected_response), 'utf-8'),
                         response.content)
