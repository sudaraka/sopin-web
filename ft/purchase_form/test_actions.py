#  ft/tests/purchase_form/test_actions.py: FT for user actions on item purchase
#  form page
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
Functional test to verify all user preformed actions on item purchase form
works.

"""

import datetime
from time import sleep

from django.core.urlresolvers import reverse

from ft.base import FunctionalTestBase

from data.models.inventory import Item


class ItemPurchaseFormVisit(FunctionalTestBase):
    """
    Test for item purchase form actions when user opens the pop-up via
    "Purchase" button on item maintenance page.

    """

    test_uri = reverse('item_maintenance')

    test_data = [
        {'name': 'test item #1', 'extended_threshold': 5, },
        {'name': 'test item #2', },
    ]

    def setUp(self):  # pylint: disable=I0011,E1002
        """ Override parent method to populate context with Item data """

        for item in self.test_data:
            Item.objects.create(**item)

        super(ItemPurchaseFormVisit, self).setUp()

    def test_submitting_form_blank_fields_show_the_error_messages(self):
        """
        Verify that hitting the submit button with quantity field blank on the
        form is showing the appropriate error message.

        """

        error_messages = [
            'Quantity cannot be blank',
            'Quantity must be a number',
        ]

        # Shopper opens the add item form
        modal = self.open_purchase_item_form(1)

        # Form shows no error messages
        for msg in error_messages:
            self.assertNotIn(msg, modal.text)

        # then she and click the submit button.
        modal.find_element_by_css_selector(
            '.modal-footer button.btn-primary').click()

        # Error message is displayed saying that name is required
        self.assertIn(error_messages[0], modal.text)

        # Then shopper start to enter a non-numeric text to quantity, and the
        # message now says that it should be a number.
        modal.find_element_by_id('id_quantity').send_keys('a')
        self.assertIn(error_messages[1], modal.text)

        # Entering a numeric value in the quantity box clears the error
        # message.
        modal.find_element_by_id('id_quantity').clear()
        modal.find_element_by_id('id_quantity').send_keys('1')
        self.assertNotIn(error_messages[0], modal.text)
        self.assertNotIn(error_messages[1], modal.text)

    def test_focus_on_date_brings_up_the_datepicker(self):
        """
        Verify the focusing on the (readonly) date field rinds up the
        datepicker dialog.

        """

        # Shopper opens the add item form
        modal = self.open_purchase_item_form(1)

        # and click on the date text box
        modal.find_element_by_id('id_date').click()

        # Datepicker pop-up is not visible
        self.assertTrue(modal.find_element_by_class_name(
            'purchase-date').is_displayed())

    def test_saved_purchas_date_show_up_in_the_items_table(self):
        """
        Verify that after adding a new purchase,the date in the item list gets
        updated.

        """

        # Shopper opens the add item form,
        modal = self.open_purchase_item_form(1)

        # enter a quantity value
        modal.find_element_by_id('id_quantity').send_keys('1')

        # then she and click the submit button.
        modal.find_element_by_css_selector(
            '.modal-footer button.btn-primary').click()

        # wait for the animation
        sleep(.1)

        # Purchase date now shows up in the item maintenance page
        self.assertIn(datetime.date.today().strftime('%B, %-d'),
                      self.browser.find_element_by_css_selector(
                          '.items-table tbody tr:nth-child(1) .last_purchase')
                      .text)
        self.assertEqual('21 days', self.browser.find_element_by_css_selector(
            '.items-table tbody tr:nth-child(1) ' + '.purchase_threshold')
            .text)
