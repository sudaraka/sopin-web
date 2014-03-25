#  data/tests/test_inventory.py: Unit tests for inventory data models
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

""" UI Unit test for inventory data models """

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from data.models.inventory import Item


class ItemModelTest(TestCase):
    """ Test "Item" data model """

    def test_default_values(self):
        """ Test if vanilla item is created with correct default values """

        item = Item()

        self.assertEqual(item.name, '')
        self.assertEqual(item.unit_symbol, '')
        self.assertEqual(item.unit_weight, 1)
        self.assertEqual(item.purchase_threshold, 21)
        self.assertEqual(item.extended_threshold, None)

    def test_saving_item_with_default_values(self):
        """ Test saving item records with default values """

        item = Item()
        item.save()

        self.assertIn(item, Item.objects.all())

    def test_blank_item_names_are_not_allowed(self):
        """
        Test application logic that prevents blank items names from being saved
        to the database.

        """

        item = Item(name='')

        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_duplicate_item_names_are_not_allowed(self):
        """
        Test application logic that prevents duplicate items names from being
        saved to the database.

        """

        Item.objects.create(name='ITEM A')
        Item.objects.create(name='ITEM B')
        item = Item(name='ITEM A')

        with self.assertRaises(IntegrityError):
            item.save()
            item.full_clean()

    def test_retrieved_items_are_sorted_by_name(self):
        """ Item retrieved back should be sorted by the name """

        i1 = Item.objects.create(name='A')
        i2 = Item.objects.create(name='C')
        i3 = Item.objects.create(name='X')
        i4 = Item.objects.create(name='B')

        self.assertEqual(list(Item.objects.all()), [i1, i4, i2, i3])
