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

from django.test import LiveServerTestCase

from selenium import webdriver


class FunctionalTestBase(LiveServerTestCase):
    """
    Base functional test class that all other functional test classes should
    derived from.
    """

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

    def tearDown(self):
        """ Cleanup test client environment after test """

        self.browser.quit()
