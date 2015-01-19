from django.conf import settings
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.select import Select

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