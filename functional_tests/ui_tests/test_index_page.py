from functional_tests.test_utils.helper import UITestCase
from integrator.models import Integration
import json
import mock

class IndexPageTest(UITestCase):
    def test_create_integration_button_rendering(self):
        self.browser.get(self.live_server_url + '/')
        self.wait_till_element_is_clickable('add_integration')
        self.browser.find_element_by_id('add_integration')

    def test_display_of_existing_integrations(self):
        integration_data = json.loads(open(self.test_data_directory + 'helpscout_integration_form.json').read())
        integration = Integration(**integration_data)
        with mock.patch('integrator.views.ui.integration.views.Integration') as integration_mock:
            integration_mock.objects.all = mock.Mock()
            conf = {'return_value': [integration]}
            integration_mock.objects.all.configure_mock(**conf)
            self.browser.get(self.live_server_url + '/')
        integration_list_element = self.browser.find_element_by_id('helpscout')
        self.assertIn('integration_detail', integration_list_element.get_attribute('class'))

    def test_navigation_index_to_create_integration_page(self):
        self.browser.get(self.live_server_url + '/')
        self.wait_till_element_is_clickable('add_integration')

        add_integration = self.browser.find_element_by_id('add_integration')
        add_integration.click()

        self.browser.back()
        add_integration = self.browser.find_element_by_id('add_integration')

