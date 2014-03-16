""" UI Unit test for homepage """

from django.test import TestCase

from app.settings import SITE_TITLE, VERSION


class HomepageTest(TestCase):
    """ Homepage unit test """

    def test_homepage_url_render_home_template(self):
        """ Url '/' should render the template 'home.html' """

        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_site_title_is_being_passed_to_the_template(self):
        """
        Verify that site title is passed to the template via response context
        """

        response = self.client.get('/')

        self.assertIn('site_title', response.context)
        self.assertEqual(response.context['site_title'], SITE_TITLE)

    def test_site_version_is_being_passed_to_the_template(self):
        """
        Verify that site version is passed to the template via response context
        """

        response = self.client.get('/')

        self.assertIn('site_version', response.context)
        self.assertEqual(response.context['site_version'], ('v%d.%d %s' %
                                                            VERSION).strip())
