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

import datetime

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from data.models.inventory import Item, Purchase


class ItemModelTest(TestCase):
    """ Test "Item" data model """

    def test_default_values(self):
        """ Test if vanilla item is created with correct default values """

        item = Item()

        self.assertEqual(item.name, '')
        self.assertEqual(item.unit_symbol, '')
        self.assertEqual(item.unit_weight, 1)
        self.assertEqual(item.purchase_threshold, 21)
        self.assertEqual(item.extended_threshold, 0)
        self.assertEqual(item.heavy, False)
        self.assertEqual(item.stock_age, None)
        self.assertEqual(item.stock_age_percent, 0)

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

    def test_item_object_contains_last_purchase_info(self):
        """
        Verify that item carries with it the information of last purchase of
        that item

        """

        item1 = Item.objects.create(name='a')
        item2 = Item.objects.create(name='b')
        Item.objects.create(name='c')

        Purchase.objects.create(item=item1, date=datetime.date(2014, 1, 1))
        item1_last_purchase = Purchase.objects.create(
            item=item1, date=datetime.date(2014, 1, 3))
        Purchase.objects.create(item=item2, date=datetime.date(2014, 1, 1))
        Purchase.objects.create(item=item1, date=datetime.date(2014, 1, 2))
        item2_last_purchase = Purchase.objects.create(
            item=item2, date=datetime.date(2014, 1, 2))

        self.assertEqual(item1.last_purchase(), item1_last_purchase)
        self.assertEqual(item2.last_purchase(), item2_last_purchase)
        self.assertEqual(Item.objects.get(pk=3).last_purchase(), None)

    def test_running_out_item_stock_age_is_correctly_calculated(self):
        """ Verify that running_out item's stock_age is correct """

        item = Item.objects.create(name='a')
        Purchase.objects.create(
            item=item, date=datetime.date.today() - datetime.timedelta(18))

        item = Item.objects.create(name='b')
        Purchase.objects.create(
            item=item, date=datetime.date.today() - datetime.timedelta(22))

        item = Item.objects.create(name='c', unit_symbol='Pkt',
                                   unit_weight=400, purchase_threshold=35,
                                   heavy=True)
        Purchase.objects.create(
            item=item, date=datetime.date.today() - datetime.timedelta(32))

        returned_items = Item.objects.running_out()

        self.assertAlmostEqual(returned_items[0].stock_age, 18, delta=.99)
        self.assertEqual(returned_items[0].stock_age_percent,
                         returned_items[0].stock_age / 21 * 100)

        self.assertAlmostEqual(returned_items[1].stock_age, 22, delta=.99)
        self.assertEqual(returned_items[1].stock_age_percent, 0)

        self.assertEqual(returned_items[2].name, 'c')
        self.assertEqual(returned_items[2].unit_symbol, 'Pkt')
        self.assertEqual(returned_items[2].unit_weight, 400)
        self.assertEqual(returned_items[2].purchase_threshold, 35)
        self.assertEqual(returned_items[2].extended_threshold, 0)
        self.assertEqual(returned_items[2].heavy, True)


class PurchaseModelTest(TestCase):
    """ Test "Purchase" data model """

    def test_default_values(self):
        """ Test if vanilla item is created with correct default values """

        item = Item()
        purchase = Purchase(item=item)

        self.assertEqual(purchase.item, item)
        self.assertEqual(purchase.quantity, 1)
        self.assertEqual(purchase.date, datetime.date.today())

    def test_saving_purchase_with_default_values(self):
        """ Test saving item records with default values """

        item = Item()
        item.save()

        purchase = Purchase(item=item)
        purchase.save()

        self.assertIn(purchase, Purchase.objects.all())

        # Date should now be populated

    def test_retrieved_purchases_are_sorted_in_reverse_order(self):
        """
        Purchases retrieved back should be sorted in the reverse order of their
        creation

        """

        item = Item.objects.create()

        p1 = Purchase.objects.create(item=item)
        p2 = Purchase.objects.create(item=item)
        p3 = Purchase.objects.create(item=item)
        p4 = Purchase.objects.create(item=item)

        self.assertEqual(list(Purchase.objects.all()), [p4, p3, p2, p1])
