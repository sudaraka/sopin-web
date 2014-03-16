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

from django.core.urlresolvers import reverse

from ft.base import FunctionalTestBase
from app.settings import SITE_TITLE, VERSION


class HomepageFirstVisit(FunctionalTestBase):
    """
    Test for homepage elements when user visit the site for the first time,
    with no user generated data.

    """

    def test_elements(self):
        """
        Verify all the required elements are available in homepage HTML.

        """

        # Shopper visit the site's homepage for the first time.
        self.browser.get(self.server_url)

        # and see the following elements on the page.
        # 1. Browser title shows the application name
        self.assertIn(SITE_TITLE, self.browser.title)

        # 2. Header with the site title which is linked to homepage.
        header = self.browser.find_element_by_tag_name('header')

        title_tag = header.find_element_by_link_text(SITE_TITLE)
        self.assertEqual(self.server_url + reverse('homepage'),
                         title_tag.get_attribute('href'))

        # 3. and links/buttons on the navigation bar to: a. Items link to
        #    master item list maintenance
        item_link = header.find_element_by_link_text('Items')
        self.assertEqual(self.server_url + reverse('item_maintenance'),
                         item_link.get_attribute('href'))

        #     b. Reports button with sub-links to each report
        report_button = header.find_element_by_css_selector('button.reports')
        self.assertEqual(report_button.text, 'Reports')

        # 4. Page have an area with the sub-heading "Shipping Rounds" which is
        #    empty at the time and showing message "No rounds scheduled". There
        #    is a "New Round" button in this area.
        area1 = self.browser.find_element_by_class_name('left-pane')
        self.assertEqual('Shipping Rounds',
                         area1.find_element_by_tag_name('h2').text)
        self.assertIn('No rounds scheduled', area1.text)
        self.assertEqual('New Round',
                         area1.find_element_by_id('btn_new_round').text)

        # 5. There is another section with the sub-heading "Items Needed" that
        #    show the message "No items needed".
        area2 = self.browser.find_element_by_class_name('right-pane')
        self.assertEqual('Items Needed',
                         area2.find_element_by_tag_name('h2').text)
        self.assertIn('No items needed', area2.text)

        # 6. Footer shows the application name, version, copyright and license
        #    information with link to source code, author contact and license
        #    web sites.
        footer = self.browser.find_element_by_tag_name('footer')

        self.assertIn(SITE_TITLE, footer.text)
        self.assertIn('v%d.%d %s' % VERSION, footer.text)
        self.assertIn('Copyright 2014 Sudaraka Wijesinghe', footer.text)
        self.assertIn('AGPL version 3 or later', footer.text)

        link = footer.find_element_by_link_text('source code')
        self.assertIn(link.get_attribute('href'),
                      ('https://github.com/sudaraka/sopin-web',
                       'https://bitbucket.com/sudaraka/sopin-web',
                       'http://git.sudaraka.org/sopin/sopin-web'))

        link = footer.find_element_by_link_text('Sudaraka Wijesinghe')
        self.assertEqual(link.get_attribute('href'),
                         'http://sudaraka.org/contact')

        link = footer.find_element_by_link_text('AGPL')
        self.assertEqual(link.get_attribute('href'),
                         'https://www.gnu.org/licenses/agpl.html')
