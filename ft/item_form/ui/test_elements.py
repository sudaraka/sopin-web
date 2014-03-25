#  ft/tests/item_form/ui/test_element.py: FT for item form page UI elements
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
Functional test to verify item form page elements while the page is in add and
edit states.

"""

from time import sleep

from django.core.urlresolvers import reverse

from ft.base import FunctionalTestBase


class AddItemPageVisit(FunctionalTestBase):
    """
    Test for item form page elements when user open the form pop-up via the
    "Add New Item" button on item maintenance page.

    """

    test_uri = reverse('item_maintenance')

    def test_elements_with_no_user_generated_content(self):
        """
        Verify all the required elements are available in form HTML.

        """

        # Shopper visit the item maintenance page, and click on the "Add New
        # Item" button.
        self.browser.find_element_by_id('btn_new_item').click()

        # wait for the animation
        sleep(.1)

        # and see form in a pop-up with the following elements:
        #
        # 1. Label and input text box for "Item Name" that shopper can enter a
        #    32 character long string, this is a mandatory field.
        label = self.browser.find_element_by_css_selector('label[for=id_name]')
        self.assertEqual('Name:', label.text)

        element = self.browser. \
            find_element_by_css_selector('input#id_name[type=text]')
        self.assertEqual('32', element.get_attribute('maxlength'))
        self.assertEqual('true', element.get_attribute('required'))

        # 2. Label and input text box for "Weight per Unit" that shopper can
        #    enter a 6 digit (excluding dot) long number. It had a default
        #    value 1 already filled in.
        label = self.browser.find_element_by_css_selector(
            'label[for=id_unit_weight]')
        self.assertEqual('Weight per Unit:', label.text)

        element = self.browser.find_element_by_css_selector(
            'input#id_unit_weight[type=text]')
        self.assertEqual('7', element.get_attribute('maxlength'))
        self.assertEqual('1', element.get_attribute('value'))

        # 3. Label and input text box for "Unit Symbol" that shopper can enter
        #    a 8 character long string.
        label = self.browser.find_element_by_css_selector(
            'label[for=id_unit_symbol]')
        self.assertEqual('Unit Symbol:', label.text)

        element = self.browser.find_element_by_css_selector(
            'input#id_unit_symbol[type=text]')
        self.assertEqual('8', element.get_attribute('maxlength'))

        # 4. Label and input text box for "Purchase Threshold" that shopper can
        #    a number, this is a mandatory field and it has a default value 21
        #    already filled in.
        label = self.browser.find_element_by_css_selector(
            'label[for=id_purchase_threshold]')
        self.assertEqual('Purchase Threshold:', label.text)

        element = self.browser.find_element_by_css_selector(
            'input#id_purchase_threshold[type=number]')
        self.assertEqual('21', element.get_attribute('value'))

        # 5. Label and input text box for "Threshold Extend" that shopper can
        #    a number.
        label = self.browser.find_element_by_css_selector(
            'label[for=id_extended_threshold]')
        self.assertEqual('Threshold Extend:', label.text)

        element = self.browser.find_element_by_css_selector(
            'input#id_extended_threshold[type=number]')

        # 6. Check box for heavy item with label text "this is a heavy item"
        label = self.browser.find_element_by_css_selector(
            'label[for=id_heavy]')
        self.assertEqual('This is a heavy item:', label.text)

        element = self.browser.find_element_by_css_selector(
            'input#id_heavy[type=checkbox]')
