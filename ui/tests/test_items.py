#  ui/tests/test_items.py: Unit tests for item maintenance page UI
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

""" UI Unit test for item maintenance page """

from django.db.models.query import QuerySet

from ui.tests.base import BaseUnitTestCase

from data.models.inventory import Item


class ItemsPageTest(BaseUnitTestCase):
    """ Item maintenance page unit test """

    uri = '/item-maintenance/'
    template = 'items/list.html'
    page_title = 'Item Maintenance'

    def test_uri_render_correct_template(self):
        """ Call base class function """

        self.uri_render_correct_template()

    def test_site_title_is_being_passed_to_the_template(self):
        """ Call base class function """

        self.site_title_is_being_passed_to_the_template()

    def test_site_version_is_being_passed_to_the_template(self):
        """ Call base class function """

        self.site_version_is_being_passed_to_the_template()

    def test_template_receives_the_item_list_via_context(self):
        """
        Item form template should have the list of Item records instance in
        it's context.

        """

        response = self.client.get(self.uri)

        self.assertIn('item_list', response.context)
        self.assertEqual(type(response.context['item_list']), type(QuerySet()))

    def test_template_receives_all_the_item_from_data_modal(self):
        """
        Template received all the items that are currently in the
        Item.objects.all() query set.

        """

        test_list = [
            Item.objects.create(name='Item A'),
            Item.objects.create(name='Item B'),
            Item.objects.create(name='Item C'),
            Item.objects.create(name='Item D'),
        ]

        response = self.client.get(self.uri)

        template_list = response.context['item_list']

        # Check if both lists have the same record count
        self.assertEqual(len(test_list), template_list.count())

        # Verify each item and list order
        for test_item in test_list:
            template_item = template_list[test_list.index(test_item)]

            self.assertEqual(test_item, template_item)
