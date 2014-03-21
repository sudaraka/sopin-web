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

from django.core.urlresolvers import reverse

from ft.base import FunctionalTestBase


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
