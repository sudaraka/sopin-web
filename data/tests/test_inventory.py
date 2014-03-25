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
