from functional_tests.test_utils.helper import UITestCase
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json

class IndexPageTest(UITestCase):
    def test_create_integration_button(self):
        self.browser.get(self.live_server_url + '/')

        try:
            wait = WebDriverWait(self.browser, 10)
            wait.until(EC.element_to_be_clickable((By.ID,'add_integration')))
        finally:
            pass

        add_integration = self.browser.find_element_by_id('add_integration')
        add_integration.click()
        create_integration_form = self.browser.find_element_by_id('create_integration_form')
        number_of_form_elements = len(create_integration_form.find_elements_by_css_selector(".form-group"))
        self.assertEquals(11, number_of_form_elements)

        self.browser.back()
        add_integration = self.browser.find_element_by_id('add_integration')