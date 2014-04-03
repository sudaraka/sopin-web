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

from django.core.urlresolvers import reverse

from ft.base import FunctionalTestBase

from data.models.inventory import Item


class ItemAddFormVisit(FunctionalTestBase):
    """
    Test for item add form actions when user opens the pop-up via "Add New
    Item" button on item maintenance page.

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
        modal = self.open_new_item_form()

        # Form shows no error messages
        for msg in error_messages:
            self.assertNotIn(msg, modal.text)

        # then she and click the submit button.
        modal.find_element_by_css_selector(
            '.modal-footer button.btn-primary').click()

        # Error message is displayed saying that name is required
        self.assertIn(error_messages[0], modal.text)

        # Then shopper start to enter a unit name, and the message disappears
        modal.find_element_by_id('id_name').send_keys('a')
        self.assertNotIn(error_messages[0], modal.text)

        # She then clears the weight filed and hits the submit button.
        modal.find_element_by_id('id_unit_weight').clear()
        modal.find_element_by_css_selector(
            '.modal-footer button.btn-primary').click()

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
            '.modal-footer button.btn-primary').click()

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

    def test_saved_form_items_show_up_in_the_items_table(self):
        """
        After adding a new item, it shows up in the table on the list table.

        """

        # Shopper opens the add item form,
        modal = self.open_new_item_form()

        # enter a unit name,
        modal.find_element_by_id('id_name').send_keys('test item #1')

        # then she and click the submit button.
        modal.find_element_by_css_selector(
            '.modal-footer button.btn-primary').click()

        # Item now shows up in the item maintenance page
        self.assertIn('test item #1',
                      self.browser.find_element_by_css_selector
                      ('div.items-table').text)

        # She add another item just to be sure
        modal = self.open_new_item_form()
        modal.find_element_by_id('id_name').send_keys('test item #2')
        modal.find_element_by_css_selector(
            '.modal-footer button.btn-primary').click()

        # Both Items are now show up in the item maintenance page
        self.assertIn('test item #1',
                      self.browser.find_element_by_css_selector
                      ('div.items-table').text)
        self.assertIn('test item #2',
                      self.browser.find_element_by_css_selector
                      ('div.items-table').text)


class ItemEditFormVisit(FunctionalTestBase):
    """
    Test for item edit form actions when user opens the pop-up via "edit"
    button on item maintenance page list.

    """

    test_uri = reverse('item_maintenance')

    test_data = [
        {'name': 'test item #1', },
        {'name': 'test item #2', },
    ]

    def setUp(self):  # pylint: disable=I0011,E1002
        """ Override parent method to populate context with Item data """

        for item in self.test_data:
            Item.objects.create(**item)

        super(ItemEditFormVisit, self).setUp()

    def test_edited_form_items_show_up_in_the_items_table(self):
        """
        After editing an existing item, the changes are applied to the table on
        the list table.

        """

        # Shopper opens the edit item form,
        modal = self.open_edit_item_form(1)

        # enter a unit name,
        modal.find_element_by_id('id_name').clear()
        modal.find_element_by_id('id_name').send_keys('test item A')

        # then she and click the submit button.
        modal.find_element_by_css_selector(
            '.modal-footer button.btn-primary').click()

        # Item now shows up in the item maintenance page with the new name
        table = self.browser.find_element_by_css_selector(
            'div.items-table table')
        self.assertIn('test item A', table.text)
        self.assertNotIn('test item #1', table.text)
        self.assertIn('test item #2', table.text)

        # She edit another item just to be sure
        # Note: "test item #2" is now on the first row because of model level
        # sorting.
        modal = self.open_edit_item_form(1)
        modal.find_element_by_id('id_name').clear()
        modal.find_element_by_id('id_name').send_keys('test item B')
        modal.find_element_by_css_selector(
            '.modal-footer button.btn-primary').click()

        # Both Items are now show up in the item maintenance page
        table = self.browser.find_element_by_css_selector(
            'div.items-table table')
        self.assertIn('test item A', table.text)
        self.assertNotIn('test item #1', table.text)
        self.assertIn('test item B', table.text)
        self.assertNotIn('test item #2', table.text)
