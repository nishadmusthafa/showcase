from django.conf import settings
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class UITestCase(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        self.test_data_directory = getattr(settings, "BASE_DIR") + '/../functional_tests/test_data/'

    def tearDown(self):
        self.browser.quit()

    def key_in_input(self, element_name, text):
        input_element = self.browser.find_element_by_id(element_name)
        input_element.send_keys(text)

    def key_in_input_by_css_selector(self, selector_string, text):
        input_element = self.browser.find_elements_by_css_selector(selector_string)[0]
        input_element.send_keys(text)

    def make_selection(self, element_name, selection_text):
        select_element = Select(self.browser.find_element_by_id(element_name))
        select_element.select_by_visible_text(selection_text)

    def check_check_box(self, element_name):
        self.browser.execute_script('$( "#'+ element_name +'" ).prop( "checked", true );')

    def uncheck_check_box(self, element_name):
        self.browser.execute_script('$( "#'+ element_name +'" ).prop( "checked", false );')

    def get_selected_item_in_dropdown(self, element_name):
        select_element = Select(self.browser.find_element_by_id('source'))
        return select_element.first_selected_option

    def get_parent_element(self, element):
        return element.find_element_by_xpath('..')

    def wait_till_element_is_clickable(self, element):
        try:
            wait = WebDriverWait(self.browser, 10)
            wait.until(EC.element_to_be_clickable((By.ID, element)))
        finally:
            pass

    def find_form_group(self, id):
        element = self.browser.find_element_by_id(id)
        while 'form-group' not in element.get_attribute('class'):
            element = self.get_parent_element(element)
        return element

    def find_help_block(self, id):
        form_group = self.find_form_group(id)
        return form_group.find_elements_by_css_selector('.help-block')[0]

    def assert_form_error_for_field(self, id, message):
        help_block = self.find_help_block(id)
        self.assertEquals(help_block.text, message)
        form_group = self.find_form_group(id)
        self.assertIn('has-error', form_group.get_attribute('class'))

    def assert_url_validation_error_for_field(self, id):
        self.assert_form_error_for_field(id, "Please key in a valid url")

    def assert_form_error_for_mandatory_field(self, id):
        self.assert_form_error_for_field(id, id + " is mandatory")

    def assert_form_is_free_of_errors(self, form):
        form = self.browser.find_element_by_id(form)
        form_groups = form.find_elements_by_css_selector('.form-group')

        for form_group in form_groups:
            self.assertNotIn('has-error', form_group.get_attribute('class'))