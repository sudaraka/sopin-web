#  ft/tests/item_form/test_actions.py: FT for user actions on item add/edit
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
Functional test to verify all user preformed actions on item add/edit form
works.

"""

from time import sleep

from django.core.urlresolvers import reverse

from ft.base import FunctionalTestBase


class ItemAddFormVisit(FunctionalTestBase):
    """
    Test for item maintenance page actions when user visit the site for the
    first time, with no user generated data.

    """

    test_uri = reverse('item_maintenance')

    def test_submitting_form_blank_fields_show_the_error_messages(self):
        """
        Verify that hitting the submit button with name, weight or threshold
        fields blank on the form is showing the appropriate error message.

        """

        error_messages = [
            'Item name cannot be blank',
            'Unit weight cannot be blank',
            'Unit weight must be a number',
            'Purchase threshold cannot be blank',
            'Purchase threshold must be a number',
        ]

        # Shopper opens the add item form
        self.browser.find_element_by_id('btn_new_item').click()

        ## wait for the animation
        sleep(.1)

        # Form shows no error messages
        modal = self.browser.find_element_by_id('div_item_form')
        for msg in error_messages:
            self.assertNotIn(msg, modal.text)

        # then she and click the submit button.
        modal.find_element_by_css_selector(
            '.modal-footer input.btn-primary').click()

        # Error message is displayed saying that name is required
        self.assertIn(error_messages[0], modal.text)

        # Then shopper start to enter a unit name, and the message disappears
        modal.find_element_by_id('id_name').send_keys('a')
        self.assertNotIn(error_messages[0], modal.text)

        # She then clears the weight filed and hits the submit button.
        modal.find_element_by_id('id_unit_weight').clear()
        modal.find_element_by_css_selector(
            '.modal-footer input.btn-primary').click()

        # Error new message is displayed saying that weight is required
        self.assertIn(error_messages[1], modal.text)

        # Then shopper start to enter a non-numeric text to weight, and the
        # message now says that it should be a number.
        modal.find_element_by_id('id_unit_weight').send_keys('a')
        self.assertIn(error_messages[2], modal.text)

        # Entering a numeric value in the weight box clears the error message.
        modal.find_element_by_id('id_unit_weight').clear()
        modal.find_element_by_id('id_unit_weight').send_keys('1')
        self.assertNotIn(error_messages[1], modal.text)
        self.assertNotIn(error_messages[2], modal.text)

        # Shopper now clears the purchase threshold box and tries to submit
        # again
        modal.find_element_by_id('id_purchase_threshold').clear()
        modal.find_element_by_css_selector(
            '.modal-footer input.btn-primary').click()

        # It now shows the error message saying purchase threshold is a
        # required field.
        self.assertIn(error_messages[3], modal.text)

        # Then she start to enter a non-numeric text to weight, and the message
        # changes to say that it should be a number.
        modal.find_element_by_id('id_purchase_threshold').send_keys('a')
        self.assertIn(error_messages[4], modal.text)

        # Entering a numeric value in the weight box clears the error message.
        modal.find_element_by_id('id_purchase_threshold').clear()
        modal.find_element_by_id('id_purchase_threshold').send_keys('1')
        self.assertNotIn(error_messages[3], modal.text)
        self.assertNotIn(error_messages[4], modal.text)

    def test_disable_the_form_while_being_submitted(self):
        """ Test submitting valid form saves the item """

        # Shopper opens the add item form,
        self.browser.find_element_by_id('btn_new_item').click()

        ## wait for the animation
        sleep(.1)

        modal = self.browser.find_element_by_id('div_item_form')

        # enter a unit name,
        modal.find_element_by_id('id_name').send_keys('test item #1')

        # then she and click the submit button.
        modal.find_element_by_css_selector(
            '.modal-footer button.btn-primary').click()

        # Form is no longer editable
        self.assertFalse(modal.find_element_by_id('id_name').is_enabled())
        self.assertFalse(modal.find_element_by_css_selector
                         ('.modal-footer button.btn-primary').is_enabled())
