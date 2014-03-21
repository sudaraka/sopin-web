#  ui/tests/base.py: Shared sub-routines for UI Unit Tests
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

""" Shared sub-routines and initialization code for UI Unit Tests """

from django.test import TestCase

from app.settings import SITE_TITLE, VERSION


class BaseUnitTestCase(TestCase):
    """
    Base unit test class that all other functional test classes should derived
    from.

    """

    # Uri to be used for the page being tested
    # IMPORTANT: This *MUST BE* hardcoded in the extended test class
    uri = None

    # Template that should be used for the page being tested
    # IMPORTANT: This *MUST BE* hardcoded in the extended test class
    template = None

    # Title of the page being tested
    # IMPORTANT: This *MUST BE* hardcoded in the extended test class
    page_title = ''

    def uri_render_correct_template(self):
        """
        Assert that when called the page uri it is rendered using the set
        template

        """

        response = self.client.get(self.uri)
        self.assertTemplateUsed(response, self.template)

    def site_title_is_being_passed_to_the_template(self):
        """
        Verify that site title is passed to the template via response context
        """

        response = self.client.get(self.uri)

        self.assertIn('site_title', response.context)

        title = SITE_TITLE
        if 0 < len(self.page_title):
            title += ' - ' + self.page_title
        self.assertEqual(response.context['site_title'], title)

    def site_version_is_being_passed_to_the_template(self):
        """
        Verify that site version is passed to the template via response context
        """

        response = self.client.get(self.uri)

        self.assertIn('site_version', response.context)
        self.assertEqual(response.context['site_version'], ('v%d.%d %s' %
                                                            VERSION).strip())
