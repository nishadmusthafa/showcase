from functional_tests.test_utils.helper import UITestCase
from integrator.models import Integration
from selenium.common.exceptions import NoSuchElementException
import contextlib
import json
import mock

class IntegrationDetailPageTest(UITestCase):
    def reach_integration_detail_page(self, integration_data_file, integration_name):
        integration_data = json.loads(open(self.test_data_directory + integration_data_file).read())
        integration = Integration(**integration_data)

        with mock.patch('integrator.views.Integration') as integration_mock:
            integration_mock.objects.all = mock.Mock()
            integration_mock.objects.get = mock.Mock()
            conf = {'return_value': [integration]}
            integration_mock.objects.all.configure_mock(**conf)
            conf = {'return_value': integration}
            integration_mock.objects.get.configure_mock(**conf)
            self.browser.get(self.live_server_url + '/')
            integration_list_element = self.browser.find_element_by_id(integration_name)
            integration_list_element.click()

    def test_page_structure(self):
        self.reach_integration_detail_page('helpscout_integration_form.json', 'helpscout')

        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Help Scout', body.text)

        integration_list_element = self.browser.find_element_by_id('json_helpscout')
        self.assertIn('integration_json', integration_list_element.get_attribute('class'))

        integration_list_element = self.browser.find_element_by_id('add_action_helpscout')
        self.assertIn('add_action', integration_list_element.get_attribute('class'))

        integration_list_element = self.browser.find_element_by_id('agent_sync_helpscout')
        self.assertIn('agent_sync', integration_list_element.get_attribute('class'))

        integration_list_element = self.browser.find_element_by_id('auth_validation_helpscout')
        self.assertIn('auth_validation', integration_list_element.get_attribute('class'))

        integration_list_element = self.browser.find_element_by_id('contact_sync_helpscout')
        self.assertIn('contact_sync', integration_list_element.get_attribute('class'))

        integration_list_element = self.browser.find_element_by_id('interaction_retrieval_helpscout')
        self.assertIn('interaction_retrieval', integration_list_element.get_attribute('class'))

    def test_navigation_integration_detail_to_index(self):
        self.reach_integration_detail_page('helpscout_integration_form.json', 'helpscout')

        self.browser.back()
        add_integration = self.browser.find_element_by_id('add_integration')

    # def test_navigation_integration_detail_to_add_actions(self):
    #     pass




