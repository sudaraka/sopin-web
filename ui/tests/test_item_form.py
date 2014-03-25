#  ui/tests/test_item_form.py: Unit tests for item add/edit form
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

""" UI Unit test for item add/edit """

from ui.tests.base import BaseUnitTestCase
from ui.forms import ItemForm


class ItemAddFormTest(BaseUnitTestCase):
    """ Item add/edit form unit test """

    uri = '/item-maintenance/form'
    template = 'items/form.html'

    def test_uri_render_correct_template(self):
        """ Call base class function """

        self.uri_render_correct_template()

    def test_template_receive_the_form_via_context(self):
        """
        Item form template should have the ItemForm instance in it's context.

        """

        response = self.client.get(self.uri)

        self.assertIn('form', response.context)
        self.assertEqual(type(response.context['form']), type(ItemForm()))
