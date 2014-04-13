#  ft/tests/items/ui/test_element.py: FT for item maintenance page UI elements
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

"""
Functional test to verify item maintenance page elements while the page is in
different states.

"""

import copy
import datetime
import random

from operator import itemgetter

from django.core.urlresolvers import reverse

from ft.base import FunctionalTestBase

from data.models.inventory import Item, Purchase


class ItemsPageVisit(FunctionalTestBase):
    """
    Test for item maintenance page elements when user visit the page via the
    link in site main navigation, with no user generated data.

    """

    test_uri = reverse('item_maintenance')

    def test_elements_with_no_user_generated_content(self):
        """
        Verify all the required elements are available in items page HTML.

        """

        # Shopper visit the item maintenance page via the link in site's main
        # navigation area, and see the following elements on the page:
        #
        # 1. Site's main header/navigation bar
        self.site_header_elements('Item Maintenance')

        # 2. Site's footer
        self.site_footer_elements()

        # 3. Page header with the heading text "Item Maintenance"
        page_header = self.browser.find_element_by_class_name('page-header')
        self.assertEqual('Item Maintenance',
                         page_header.find_element_by_tag_name('h3').text)

        # 4. Button next to the heading to "Add New Item".
        self.assertEqual('Add New Item',
                         page_header.find_element_by_id('btn_new_item').text)

        # 5. Text "no items available"
        table_div = self.browser.find_element_by_class_name('items-table')
        self.assertIn('No items available', table_div.text)


class ItemsPageVisitWithData(FunctionalTestBase):
    """
    Test for item maintenance page elements when user visit the page via the
    link in site main navigation, with few items records already in context.

    """

    test_uri = reverse('item_maintenance')

    test_data = [
        {'name': 'TEST #1', },
        {'name': 'TEST #2', 'unit_symbol': 'Bottel', 'heavy': True,
         'last_purchase': datetime.date(2013, 9, 28)},
        {'name': 'TEST #4', 'unit_symbol': 'Pkt', 'unit_weight': 200,
         'purchase_threshold': 10,
         'last_purchase': datetime.date(2014, 2, 16)},
        {'name': 'TEST #3', 'unit_weight': 400, 'purchase_threshold': 15,
         'extended_threshold': 4, 'heavy': True, },
    ]

    def setUp(self):  # pylint: disable=I0011,E1002
        """ Override parent method to populate context with Item data """

        for item in self.test_data:
            i = copy.copy(item)

            if 'last_purchase' in i:
                del i['last_purchase']

            created_item = Item.objects.create(**i)

            if 'last_purchase' in item:
                Purchase.objects.create(item=created_item,
                                        quantity=random.randrange(1, 11),
                                        date=item['last_purchase'])

        super(ItemsPageVisitWithData, self).setUp()

    def test_elements_with_item_records(self):
        """ Verify that all page elements are present with item records """

        # Shopper visit the page with some item data already in the context.
        # and see the following elements on the page:
        #
        # 1. There is a table with records
        table = self.browser.find_element_by_css_selector('.items-table table')

        # 2. Table shows Name, Unit Symbol, Weight, Thresholds and edit,
        #    removed buttons
        head = table.find_element_by_tag_name('thead')
        self.assertIn('Name', head.text)
        self.assertIn('Unit Symbol', head.text)
        self.assertIn('Unit Weight', head.text)
        self.assertIn('Purchase Threshold', head.text)
        self.assertIn('Last Purchase', head.text)

        stored_items = Item.objects.all().values()

        check_list = sorted(self.test_data, key=itemgetter('name'))
        for item in check_list:
            row_index = check_list.index(item) + 1

            for k in item:
                if k in ['extended_threshold', 'last_purchase_qty',
                         'last_purchase']:
                    continue

                if 'heavy' == k and item[k]:
                    cell = table.find_element_by_css_selector(
                        'tbody tr:nth-child(%d) td.unit_weight' % row_index)

                    self.assertIn('fa-anchor',
                                  cell.find_element_by_tag_name('small')
                                  .get_attribute('class'))
                else:
                    if 'purchase_threshold' == k and \
                            'extended_threshold' in item:
                        item[k] += item['extended_threshold']

                    cell = table.find_element_by_css_selector(
                        'tbody tr:nth-child(%d) td.%s' % (row_index, k))

                    self.assertIn(str(item[k]), cell.text)

            last_purchase_text = ''

            if 'last_purchase' in item:
                last_purchase_text = \
                    item['last_purchase'].strftime('%B, %-d')
            else:
                last_purchase_text = 'n/a'

            self.assertIn(last_purchase_text,
                          table.find_element_by_css_selector(
                              'tbody tr:nth-child(%d) .last_purchase' %
                              row_index).text)

            # Test Edit button
            button = table.find_element_by_css_selector(
                'tbody tr:nth-child(%d) .btn-edit' % row_index)

            self.assertEqual(reverse('item_maintenance_form',
                                     args=(stored_items[row_index - 1]['id'],
                                           )),
                             button.get_attribute('data-remote'))

            # Test Delete button
            button = table.find_element_by_css_selector(
                'tbody tr:nth-child(%d) .btn-delete' % row_index)

            self.assertEqual(reverse('item_maintenance_delete',
                                     args=(stored_items[row_index - 1]['id'],
                                           )),
                             button.get_attribute('data-url'))

            # Test Purchase button
            button = table.find_element_by_css_selector(
                'tbody tr:nth-child(%d) .btn-purchase' % row_index)

            self.assertEqual(reverse('item_purchase_form') + '?item=' +
                             str(stored_items[row_index - 1]['id']),
                             button.get_attribute('data-remote'))
