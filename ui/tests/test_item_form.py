#  ui/tests/test_item_form.py: Unit tests for item add/edit form
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

""" UI Unit test for item add/edit """

import random
import json

from ui.tests.base import BaseUnitTestCase

from ui.forms import ItemForm

from data.models.inventory import Item


class ItemAddFormTest(BaseUnitTestCase):
    """ Item add form unit test """

    uri = '/item-maintenance/form/'
    template = 'items/form.html'

    def test_uri_render_correct_template(self):
        """ Call base class function """

        self.uri_render_correct_template()

    def test_template_receive_the_form_via_context(self):
        """
        Item form template should have the ItemForm instance in it's context.

        """

        response = self.client.get(self.uri)

        self.assertIn('form', response.context)
        self.assertEqual(type(response.context['form']), type(ItemForm()))

    def test_form_POST_saves_the_new_item(self):
        """ Make sure we can create and save new item by posting the form. """

        # Note: values are convened here to simulate how they are submitted
        # by a web browser
        post_data = {
            'name': 'Test Item #' + str(random.randint(1000, 9999)),
            'unit_symbol': random.choice(['K', 'pkt', 'bottle', 'block']),
            'unit_weight': str(random.randint(1000, 9999)),
            'purchase_threshold': str(random.randint(10, 99)),
            'extended_threshold': str(random.randint(10, 99)),
        }

        self.client.post(self.uri, data=post_data)

        # Verify that we have one item stored
        self.assertEqual(Item.objects.count(), 1)

        # Verify the saved item has the same information posted
        saved_item = Item.objects.first()
        self.assertEqual(saved_item.name, post_data['name'])
        self.assertEqual(saved_item.unit_symbol, post_data['unit_symbol'])
        self.assertEqual(saved_item.unit_weight, int(post_data['unit_weight']))
        self.assertEqual(saved_item.purchase_threshold,
                         int(post_data['purchase_threshold']))
        self.assertEqual(saved_item.extended_threshold,
                         int(post_data['extended_threshold']))

    def test_item_data_POST_return_JSON_response(self):
        """ Test if POSTing data to item form returns a valid JSON reponse """

        post_data = {
            'name': 'Test Item #' + str(random.randint(1000, 9999)),
            'unit_symbol': random.choice(['K', 'pkt', 'bottle', 'block']),
            'unit_weight': str(random.randint(1000, 9999)),
            'purchase_threshold': str(random.randint(10, 99)),
            'extended_threshold': str(random.randint(10, 99)),
        }
        response = self.client.post(self.uri, data=post_data)

        self.assertIn('application/json', response['Content-Type'])

        expected_response = {
            'code': 0,
            'message': 'success',
        }

        self.assertEqual(bytes(json.dumps(expected_response), 'utf-8'),
                         response.content)


class ItemEditFormWithNonExistingItemIDTest(ItemAddFormTest):
    """
    Item edit form with invalid (non-existing) item ID passed in. This *must*
    fall-back to "add" mode gracefully.

    """

    uri = '/item-maintenance/form/999/'


class ItemEditFormTest(BaseUnitTestCase):
    """ Item edit form with valid item ID passed in. """

    uri = '/item-maintenance/form/2/'
    template = 'items/form.html'

    def test_uri_render_correct_template(self):
        """ Call base class function """

        Item.objects.create(name='Test Item A')
        Item.objects.create(name='Test Item B')
        Item.objects.create(name='Test Item C')

        self.uri_render_correct_template()

    def test_template_receive_the_form_via_context(self):
        """
        Item form template should have the ItemForm instance in it's context.

        """

        Item.objects.create(name='Test Item A')
        Item.objects.create(name='Test Item B')
        Item.objects.create(name='Test Item C')

        response = self.client.get(self.uri)

        self.assertIn('form', response.context)
        self.assertEqual(response.context['form'].instance,
                         Item.objects.get(id=2))

    def test_form_POST_updates_an_existing_item(self):
        """ Make sure we can update and existing item by posting the form. """

        Item.objects.create(name='Test Item A')
        Item.objects.create(name='Test Item B')

        # Note: values are convened here to simulate how they are submitted
        # by a web browser
        post_data = {
            'id': 2,
            'name': 'Test Item C',
            'unit_symbol': random.choice(['K', 'pkt', 'bottle', 'block']),
            'unit_weight': str(random.randint(1000, 9999)),
            'purchase_threshold': str(random.randint(10, 99)),
            'extended_threshold': str(random.randint(10, 99)),
        }

        self.client.post(self.uri, data=post_data)

        # Verify that we have one item stored
        self.assertEqual(Item.objects.count(), 2)

        # Verify the saved item has the same information posted
        saved_item = Item.objects.last()
        self.assertEqual(saved_item.name, post_data['name'])
        self.assertEqual(saved_item.unit_symbol, post_data['unit_symbol'])
        self.assertEqual(saved_item.unit_weight, int(post_data['unit_weight']))
        self.assertEqual(saved_item.purchase_threshold,
                         int(post_data['purchase_threshold']))
        self.assertEqual(saved_item.extended_threshold,
                         int(post_data['extended_threshold']))

        # Verify the other item has  not changed
        saved_item = Item.objects.first()
        self.assertEqual(saved_item.name, 'Test Item A')
        self.assertEqual(saved_item.unit_symbol, '')
        self.assertEqual(saved_item.unit_weight, 1)
        self.assertEqual(saved_item.purchase_threshold, 21)
        self.assertEqual(saved_item.extended_threshold, 0)
