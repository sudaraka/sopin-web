#  ft/tests/purchase_form/ui/test_element.py: FT for item purchase form page UI
#  elements
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

""" Functional test to verify item purchase form page elements. """

import datetime

from time import sleep

from django.core.urlresolvers import reverse

from ft.base import FunctionalTestBase


class PurchaseFormVisit(FunctionalTestBase):
    """
    Test for item purchase form page elements when user open the form pop-up
    via the "purchase" button on item maintenance page.

    """

    test_uri = reverse('item_maintenance')

    test_data_items = [
        {'name': 'TEST #1', },
        {'name': 'TEST #3', },
        {'name': 'TEST #2', 'unit_symbol': 'Bottle', 'unit_weight': 23,
         'purchase_threshold': 40, 'extended_threshold': 3, 'heavy': True, },
    ]

    def test_elements_with_no_user_generated_content(self):
        """
        Verify all the required elements are available in form HTML.

        """

        # Shopper visit the item maintenance page, and click on the "purchase"
        # button in first row of the table.
        self.open_purchase_item_form(1)

        # and see form in a pop-up with the following elements:
        #
        # 1. Summary of the item that is being purchased.
        h = self.browser.find_element_by_class_name('modal-title')

        self.assertEqual('Purchase: TEST #1 1g', h.text)

        # 1. "Date" Input element with todays date as the value
        element = self.browser. \
            find_element_by_css_selector('input#id_date[type=text]')
        self.assertEqual(datetime.date.today().strftime('%Y-%m-%d'),
                         element.get_attribute('value'))

        # 3. "Quantity" element with empty value
        element = self.browser. \
            find_element_by_css_selector('input#id_quantity')
        self.assertEqual('', element.get_attribute('value'))

        # She closes the pop-up form and click on the "purchase" button in
        # second row of the table.
        self.browser.find_element_by_css_selector(
            '.modal-footer button[type=button].btn-default').click()

        # wait for the animation
        sleep(.3)

        self.open_purchase_item_form(2)

        # and see form in a pop-up with the following elements:
        #
        # 1. Summary of the item that is being purchased.
        h = self.browser.find_element_by_class_name('modal-title')

        self.assertEqual('Purchase: TEST #2 23g Bottle', h.text)

        # 1. "Date" Input element with todays date as the value
        element = self.browser. \
            find_element_by_css_selector('input#id_date[type=text]')
        self.assertEqual(datetime.date.today().strftime('%Y-%m-%d'),
                         element.get_attribute('value'))

        # 3. "Quantity" element with empty value
        element = self.browser. \
            find_element_by_css_selector('input#id_quantity')
        self.assertEqual('', element.get_attribute('value'))
