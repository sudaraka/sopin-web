#  ft/tests/homepage/ui/test_element.py: FT for homepage UI elements
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
Functional test to verify homepage elements while the page is in different
states.

"""

from ft.base import FunctionalTestBase


class HomepageFirstVisit(FunctionalTestBase):
    """
    Test for homepage elements when user visit the site for the first time,
    with no user generated data.

    """

    def test_elements_with_no_user_generated_content(self):
        """
        Verify all the required elements are available in homepage HTML.

        """

        # Shopper visit the site's homepage for the first time, and see the
        # following elements on the page.
        #
        # 1. Site's main header/navigation bar
        self.site_header_elements()

        # 2. Site's footer
        self.site_footer_elements()

        # 3. Page have an area with the sub-heading "Shopping Rounds" which is
        #    empty at the time and showing message "No rounds scheduled". There
        #    is a "New Round" button in this area.
        area1 = self.browser.find_element_by_class_name('left-pane')
        self.assertEqual('Shopping Rounds',
                         area1.find_element_by_tag_name('h3').text)
        self.assertIn('No rounds scheduled', area1.text)
        self.assertEqual('New Round',
                         area1.find_element_by_id('btn_new_round').text)

        # 3. There is another section with the sub-heading "Items Needed" that
        #    show the message "No items available".
        area2 = self.browser.find_element_by_class_name('right-pane')
        self.assertEqual('Available Items',
                         area2.find_element_by_tag_name('h3').text)
        self.assertIn('No items available', area2.text)
