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

import datetime

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

        # 4. On the right hand side of the screen, there is a section titled
        #    "Items to Buy" which shows the message "No items need buying"
        area2 = self.browser.find_element_by_class_name('right-pane')
        self.assertEqual('Items to Buy',
                         area2.find_element_by_css_selector('.to-buy h3').text)
        self.assertIn('No items need buying', area2.text)

        # 5. Just under the "Items to Buy" section, there is another section
        #    with the sub-heading "Items Running Out" that show the message "No
        #    items running out".
        self.assertEqual('Items Running Out',
                         area2.find_element_by_css_selector('.running-out h3')
                         .text)
        self.assertIn('No items running out', area2.text)


class HomepageVisitWithRunningOutItemData(FunctionalTestBase):
    """
    Test for homepage elements when user visit the site with the inventory
    containing items that run out soon.

    """

    test_data_items = [
        # Item without purchase
        {'name': 'test item A', },

        # Item passed threshold
        {'name': 'test item B', 'quantity': 1,
         'last_purchase': datetime.date.today() - datetime.timedelta(22), },

        # Item purchased few weeks ago (in threshold, running out)
        {'name': 'test item C', 'quantity': 1,
         'last_purchase': datetime.date.today() - datetime.timedelta(20), },

        # 2 Items purchased few weeks ago (NOT in threshold, NOT running out)
        {'name': 'test item C2', 'quantity': 2,
         'last_purchase': datetime.date.today() - datetime.timedelta(20), },

        # Item purchased few days ago (in threshold, NOT running out)
        {'name': 'test item D', 'quantity': 1,
         'last_purchase': datetime.date.today() - datetime.timedelta(11), },
        {'name': 'test item E', 'quantity': 1,
         'last_purchase': datetime.date.today() - datetime.timedelta(9), },
        {'name': 'test item F', 'quantity': 1,
         'last_purchase': datetime.date.today() - datetime.timedelta(5), },

        # Same data with non-default threshold
        {'name': 'test item G', 'purchase_threshold': 10, 'quantity': 1,
         'last_purchase': datetime.date.today() - datetime.timedelta(22), },
        {'name': 'test item H', 'purchase_threshold': 10, 'quantity': 1,
         'last_purchase': datetime.date.today() - datetime.timedelta(20), },
        {'name': 'test item I', 'purchase_threshold': 10, 'quantity': 1,
         'last_purchase': datetime.date.today() - datetime.timedelta(11), },
        {'name': 'test item J', 'purchase_threshold': 10, 'quantity': 1,
         'last_purchase': datetime.date.today() - datetime.timedelta(9), },
        {'name': 'test item J2', 'purchase_threshold': 10, 'quantity': 2,
         'last_purchase': datetime.date.today() - datetime.timedelta(9), },
        {'name': 'test item K', 'purchase_threshold': 10, 'quantity': 1,
         'last_purchase': datetime.date.today() - datetime.timedelta(5), },
    ]

    def test_elements_in_right_column(self):
        """
        Verify all the required elements are available in homepage HTML.

        """

        # Shopper visit the site later with some items that run out soon
        # already in the inventory.
        #
        # 1. Them message that was there before saying "no items" is now gone
        area = self.browser.find_element_by_css_selector(
            '.right-pane .running-out')
        self.assertNotIn('No items running out', area.text)

        # 2. The correct items are listed in the "Items Running Out" list.
        self.assertIn('test item C',
                      area.find_element_by_class_name('list-group').text)
        self.assertIn('test item J',
                      area.find_element_by_class_name('list-group').text)
        self.assertIn('test item K',
                      area.find_element_by_class_name('list-group').text)

        for item in self.test_data_items:
            if item['name'] in ['test item C', 'test item J', 'test item K', ]:
                continue

            self.assertNotIn(
                item['name'],
                area.find_element_by_class_name('list-group').text)


class HomepageVisitWithThresholdPassedItemData(FunctionalTestBase):
    """
    Test for homepage elements when user visit the site with the inventory
    containing items that already passed the purchase threshold.

    """

    test_data_items = [
        # Item without purchase
        {'name': 'test item A', },

        # Item passed threshold
        {'name': 'test item B', 'quantity': 1,
         'last_purchase': datetime.date.today() - datetime.timedelta(22), },

        # 2 Items purchased (should not need to buy)
        {'name': 'test item B2', 'quantity': 2,
         'last_purchase': datetime.date.today() - datetime.timedelta(22), },

        # Item purchased few weeks ago (in threshold, running out)
        {'name': 'test item C', 'quantity': 1,
         'last_purchase': datetime.date.today() - datetime.timedelta(20), },

        # Item purchased few days ago (in threshold, NOT running out)
        {'name': 'test item D', 'quantity': 1,
         'last_purchase': datetime.date.today() - datetime.timedelta(11), },
        {'name': 'test item E', 'quantity': 1,
         'last_purchase': datetime.date.today() - datetime.timedelta(9), },
        {'name': 'test item F', 'quantity': 1,
         'last_purchase': datetime.date.today() - datetime.timedelta(5), },

        # Same data with non-default threshold
        {'name': 'test item G', 'purchase_threshold': 10, 'quantity': 1,
         'last_purchase': datetime.date.today() - datetime.timedelta(22), },
        {'name': 'test item G2', 'purchase_threshold': 10, 'quantity': 3,
         'last_purchase': datetime.date.today() - datetime.timedelta(22), },
        {'name': 'test item H', 'purchase_threshold': 10, 'quantity': 1,
         'last_purchase': datetime.date.today() - datetime.timedelta(20), },
        {'name': 'test item I', 'purchase_threshold': 10, 'quantity': 1,
         'last_purchase': datetime.date.today() - datetime.timedelta(11), },
        {'name': 'test item J', 'purchase_threshold': 10, 'quantity': 1,
         'last_purchase': datetime.date.today() - datetime.timedelta(9), },
        {'name': 'test item K', 'purchase_threshold': 10, 'quantity': 1,
         'last_purchase': datetime.date.today() - datetime.timedelta(5), },
    ]

    def test_elements_in_right_column(self):
        """
        Verify all the required elements are available in homepage HTML.

        """

        # Shopper visit the site later with some items that already passed
        # purchase threshold in the inventory.
        #
        # 1. Them message that was there before saying "no items" is now gone
        area = self.browser.find_element_by_css_selector(
            '.right-pane .to-buy')
        self.assertNotIn('No items need buying', area.text)

        # 2. The correct items are listed in the "Items to Buy" list.
        self.assertIn('test item A',
                      area.find_element_by_class_name('list-group').text)
        self.assertIn('test item B',
                      area.find_element_by_class_name('list-group').text)
        self.assertIn('test item G',
                      area.find_element_by_class_name('list-group').text)
        self.assertIn('test item H',
                      area.find_element_by_class_name('list-group').text)
        self.assertIn('test item I',
                      area.find_element_by_class_name('list-group').text)

        for item in self.test_data_items:
            if item['name'] in ['test item A', 'test item B', 'test item G',
                                'test item H', 'test item I', ]:
                continue

            self.assertNotIn(
                item['name'],
                area.find_element_by_class_name('list-group').text)

        # 3. There's also a download button next to the "Items to Buy" header.
        button = area.find_element_by_css_selector('.page-header button')

        self.assertIn(
            'fa-download',
            button.find_element_by_tag_name('i').get_attribute('class'))
