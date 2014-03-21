#  ft/tests/homepage/test_actions.py: FT for user actions on homepage
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
Functional test to verify all user preformed actions on home page works.

"""

from django.core.urlresolvers import reverse

from ft.base import FunctionalTestBase


class HomepageFirstVisit(FunctionalTestBase):
    """
    Test for homepage actions when user visit the site for the first time,
    with no user generated data.

    """

    def test_items_button(self):
        """
        Verify that "Items" button takes the user to "Item Maintenance" page.

        """

        # Shopper visit the site's homepage for the first time, and click on
        # the "Items" link on the main navigation bar
        self.browser.find_element_by_partial_link_text('Items').click()

        self.assertEqual(self.server_url + reverse('item_maintenance'),
                         self.browser.current_url)
