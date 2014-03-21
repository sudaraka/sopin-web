#  ft/tests/homepage/ui/test_layout.py: FT for homepage UI layout
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
Functional test to verify homepage layout while the page is in different
states.

"""

from ft.base import FunctionalTestBase


class HomepageFirstVisit(FunctionalTestBase):
    """
    Test for homepage layout when user visit the site for the first time,
    with no user generated data.

    """

    def test_layout(self):
        """
        Verify all the main areas of the homepage is positioned correctly.

        """

        # Shopper visit the site's homepage for the first time.
        viewport = self.browser.get_window_size()

        # and notices following areas in the home page
        # 1. Navigation bar on top of the page with:
        navbar = self.browser.find_element_by_css_selector('header.navbar')
        self.assertEqual(navbar.location['x'], 0)
        self.assertEqual(navbar.location['y'], 0)

        #   a. Site title at the left
        self.assertEqual(
            navbar.find_element_by_class_name('navbar-brand').location['x'], 0)

        #   b. and set of links aligned to right edge
        toolbar = navbar.find_element_by_class_name('navbar-nav')
        self.assertAlmostEqual(toolbar.location['x'], viewport['width'] -
                               toolbar.size['width'], delta=10)

        # 2. Tow columns side-by-side in middle of the page, where right column
        #    is about 25% of the page width and left column filling the rest.
        left_pane = self.browser.find_element_by_class_name('left-pane')
        self.assertAlmostEqual(viewport['width'] * .75,
                               left_pane.size['width'], delta=1)
        self.assertEqual(left_pane.location['x'], 0)

        right_pane = self.browser.find_element_by_class_name('right-pane')
        self.assertAlmostEqual(viewport['width'] * .25,
                               right_pane.size['width'], delta=1)
        self.assertAlmostEqual(right_pane.location['x'], viewport['width'] *
                               .75, delta=1)

        # 3. Footer at the bottom of the page with single line of text
        footer = self.browser.find_element_by_tag_name('footer')
        self.assertEqual(footer.location['x'], 0)
        self.assertAlmostEqual(footer.size['height'], 49, delta=5)
