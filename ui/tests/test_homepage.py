#  ui/tests/test_homepage.py: Unit tests for homepage UI
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

""" UI Unit test for homepage """

import datetime

from ui.tests.base import BaseUnitTestCase

from data.models.inventory import Item, Purchase


class HomepageTest(BaseUnitTestCase):
    """ Homepage unit test """

    uri = '/'
    template = 'home.html'

    def test_uri_render_correct_template(self):
        """ Call base class function """

        self.uri_render_correct_template()

    def test_site_title_is_being_passed_to_the_template(self):
        """ Call base class function """

        self.site_title_is_being_passed_to_the_template()

    def test_site_version_is_being_passed_to_the_template(self):
        """ Call base class function """

        self.site_version_is_being_passed_to_the_template()

    def test_receives_the_running_out_list_via_context(self):
        """
        Homepage template should have the list of running out item records
        instance in it's context.

        """

        item = Item.objects.create(name='Test #1')
        Purchase.objects.create(
            item=item, date=datetime.date.today() - datetime.timedelta(22))

        item = Item.objects.create(name='Test #2')
        Purchase.objects.create(
            item=item, date=datetime.date.today() - datetime.timedelta(16))

        response = self.client.get(self.uri)

        self.assertIn('running_out_list', response.context)
        self.assertEqual(type(response.context['running_out_list']),
                         type([]))
        self.assertEqual(len(response.context['running_out_list']), 1)
