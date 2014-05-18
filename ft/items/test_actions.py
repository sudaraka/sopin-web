#  ft/tests/items/test_actions.py: FT for user actions on items maintenance
#  page
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
Functional test to verify all user preformed actions on item maintenance page
works.

"""

from time import sleep

from django.core.urlresolvers import reverse

from ft.base import FunctionalTestBase


class ItemsPageVisit(FunctionalTestBase):
    """
    Test for item maintenance page actions when user visit the site for the
    first time, with no user generated data.

    """

    test_uri = reverse('item_maintenance')

    def test_add_new_button_displays_form_popup(self):
        """
        Verify that "Add New Item" button opens the pop-up for item form.

        """

        # Shopper visit the item maintenance page for the first time, and click
        # on the "Add New Item" button
        self.browser.find_element_by_id('btn_new_item').click()

        # wait for the animation
        sleep(.2)

        modal = self.browser.find_element_by_id('div_modal_form')
        self.assertTrue(modal.is_displayed())
        self.assertIn('New Item', modal.text)


class ItemsPageVisitWithData(FunctionalTestBase):
    """
    Test for item maintenance page actions when user visit the page with few
    item records already in context.

    """

    test_uri = reverse('item_maintenance')

    test_data_items = [
        {'name': 'test item #1', 'extended_threshold': 4},
        {'name': 'test item #3', 'unit_symbol': 'Bottle'},
        {'name': 'test item #2', 'unit_weight': 5000, 'heavy': True},
    ]

    def test_edit_button_displays_form_popup_with_record_information(self):
        """
        Verify that "Edit" button opens the pop-up for item form with record
        data already populated.

        """

        # Shopper visit the item maintenance page and see number of items on
        # the listing page. She clicks on the "Edit" button on the first item.
        self.browser.find_element_by_css_selector(
            '.items-table table tr:nth-child(1) button.btn-edit').click()

        # wait for the animation
        sleep(.2)

        modal = self.browser.find_element_by_id('div_modal_form')

        self.assertTrue(modal.is_displayed())
        self.assertIn('Edit Item', modal.text)

    def test_delete_button_displays_confirmation_popup_with_message(self):
        """
        Verify that "Delete" button opens the pop-up for confirmation with
        record name.

        """

        # Shopper visit the item maintenance page and see number of items on
        # the listing page. She clicks on the "Delete" button on the second
        # item.
        modal = self.open_delete_confirmation_dialog(2)

        self.assertTrue(modal.is_displayed())
        self.assertIn('Remove item ' + self.test_data_items[2]['name'] + '?',
                      modal.text)

    def test_no_button_on_confirmation_popup_closes_it_without_change(self):
        """
        Verify that clicking no button on delete confirmation dialog returns
        the user to item list without any change.

        """

        # Shopper visit the item maintenance page and clicks on the "Delete"
        # button on an item.
        modal = self.open_delete_confirmation_dialog(1)

        modal.find_element_by_css_selector(
            '.modal-footer button[data-dismiss=modal]').click()

        table = self.browser.find_element_by_css_selector(
            '.items-table table tbody')

        for i in self.test_data_items:
            self.assertIn(i['name'], table.text)

    def test_yes_button_on_confirmation_popup_removes_the_item_from_list(self):
        """
        Verify that clicking yes button on delete confirmation dialog returns
        the user to item list with the selected item removed.

        """

        # Shopper visit the item maintenance page and clicks on the "Delete"
        # button on an item.
        modal = self.open_delete_confirmation_dialog(1)

        modal.find_element_by_id('lnk_delete_confirm').click()

        table = self.browser.find_element_by_css_selector(
            '.items-table table tbody')

        for i in self.test_data_items:
            if self.test_data_items.index(i) == 0:
                self.assertNotIn(i['name'], table.text)
            else:
                self.assertIn(i['name'], table.text)

        self.assertIn('Item was successfully removed',
                      self.browser.find_element_by_css_selector(
                          'p.row.alert').text)

    def test_purchase_button_displays_form_popup_with_item_and_inputs(self):
        """
        Verify that "Purchase" button opens the pop-up for item purchase form
        with item data already populated.

        """

        # Shopper visit the item maintenance page and see number of items on
        # the listing page. She clicks on the "Purchase" button on the first
        # item.
        modal = self.open_purchase_item_form(1)

        self.assertTrue(modal.is_displayed())
        self.assertIn('Purchase: test item #1 1g', modal.text)
