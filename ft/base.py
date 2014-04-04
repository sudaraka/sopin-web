#  ft/base.py: Shared sub-routines and initialization code for Functional Tests
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

""" Shared sub-routines and initialization code for Functional Tests """

import sys
from time import sleep

from django.test import LiveServerTestCase
from django.core.urlresolvers import reverse

from selenium import webdriver

from app.settings import SITE_TITLE, VERSION


class FunctionalTestBase(LiveServerTestCase):
    """
    Base functional test class that all other functional test classes should
    derived from.
    """

    # When test_uri contains a non None value, browser will be navigate to
    # server_url + test_uri.
    test_uri = None

    @classmethod
    def setUpClass(cls):
        """ Initialize test client environment for all tests """

        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]

                return

        LiveServerTestCase.setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        """ Cleanup test client environment after all tests """

        if cls.server_url == cls.live_server_url:
            LiveServerTestCase.tearDownClass()

    def setUp(self):
        """ Initialize test client environment for each test """

        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        self.browser.set_window_size(1024, 768)

        url = self.server_url

        if self.test_uri is not None:
            url += self.test_uri

        self.browser.get(url)

    def tearDown(self):
        """ Cleanup test client environment after test """

        self.browser.quit()

    def site_header_elements(self, browser_title=''):
        """
        Check if current browser page content contains the site header and all
        common components. Returns the header webelement to the caller after
        initial tests.

        """

        # 1. Browser title shows the application name and "Item Maintenance"
        title = SITE_TITLE
        if 0 < len(browser_title):
            title += ' - ' + browser_title

        self.assertIn(title, self.browser.title)

        # 2. Header with the site title which is linked to homepage.
        header = self.browser.find_element_by_tag_name('header')

        title_tag = header.find_element_by_partial_link_text(SITE_TITLE)
        self.assertEqual(self.server_url + reverse('homepage'),
                         title_tag.get_attribute('href'))

        # 3. and links/buttons on the navigation bar to:
        #     a. Items link to master item list maintenance
        item_link = header.find_element_by_partial_link_text('Items')
        self.assertEqual(self.server_url + reverse('item_maintenance'),
                         item_link.get_attribute('href'))

        #     b. Reports button with sub-links to each report
        report_button = header.find_element_by_partial_link_text('Reports')
        self.assertEqual(self.browser.current_url + '#',
                         report_button.get_attribute('href'))

        return header

    def site_footer_elements(self):
        """
        Check if current browser page content contains the site footer and all
        common components. Returns the footer webelement to the caller after
        initial tests.

        """

        # Footer shows the application name, version, copyright and license
        # information with link to source code, author contact and license web
        # sites.
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

        return footer

    def open_new_item_form(self):
        """
        Open the item add form by clicking the "add new" button, and
        return the modal dialog element that opens.

        """

        # Shopper opens the add item form
        self.browser.find_element_by_id('btn_new_item').click()

        # # wait for the animation
        sleep(.1)

        return self.browser.find_element_by_id('div_item_form')

    def open_edit_item_form(self, from_item_list_row):
        """
        Open the item edit form by clicking the "edit" button, and return the
        modal dialog element that opens.

        """

        # Shopper opens the edit item form
        self.browser.find_element_by_css_selector(
            '.items-table tr:nth-child(%d) .btn-edit' %
            from_item_list_row).click()

        # # wait for the animation
        sleep(.1)

        return self.browser.find_element_by_id('div_item_form')

    def open_delete_confirmation_dialog(self, from_item_list_row):
        """
        Open the item delete confirmation dialog by clicking the "delete"
        button, and return the modal dialog element that opens.

        """

        # Shopper opens the delete item form
        self.browser.find_element_by_css_selector(
            '.items-table tr:nth-child(%d) .btn-delete' %
            from_item_list_row).click()

        # # wait for the animation
        sleep(.1)

        return self.browser.find_element_by_id('div_item_delete')
