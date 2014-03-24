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
        sleep(.1)

        modal = self.browser.find_element_by_id('div_item_form')
        self.assertTrue(modal.is_displayed())
        self.assertIn('New Item', modal.text)
