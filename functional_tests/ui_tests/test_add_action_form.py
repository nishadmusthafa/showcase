from functional_tests.test_utils.helper import UITestCase
from selenium.common.exceptions import NoSuchElementException
from integrator.views.ui.action.views import Action, Integration
import json
import mock
from mongoengine.errors import NotUniqueError


class ActionFormTest(UITestCase):
    def json_to_input_param_form(self, data_file_path):
        input_params = json.loads(open(data_file_path).read())
        self.key_in_input("key", input_params.get("key", ""))
        self.key_in_input_by_css_selector("#input_param_form #name", input_params.get("name", ""))
        if input_params["mandatory"]:
            self.check_check_box("mandatory")
        else:
            self.uncheck_check_box("mandatory")

    def json_to_action_form(self, data_file_path):
        action_form_data = json.loads(open(data_file_path).read())
        self.key_in_input("name", action_form_data.get("name", ""))
        self.key_in_input("display", action_form_data.get("display", ""))
        self.key_in_input("http_url", action_form_data.get("http_url", ""))
        self.key_in_input("basic_auth", action_form_data.get("basic_auth", ""))
        self.key_in_input("http_request_params", action_form_data.get("http_request_params", ""))
        self.key_in_input("success_response", action_form_data.get("success_response", ""))

    def clear_input_param_form(self):
        self.browser.find_element_by_id('key').clear()
        self.browser.find_elements_by_css_selector("#input_param_form #name")[0].clear()
        self.uncheck_check_box("mandatory")

    def input_param_form_to_json(self):
        input_param_data = {
                    "key": self.browser.find_element_by_id('key').get_attribute('value'),
                    "name": self.browser.find_elements_by_css_selector("#input_param_form #name")[0].get_attribute('value'),
                    "mandatory": self.browser.find_element_by_id('mandatory').get_attribute("checked") == "true"
                }
        return input_param_data

    def dismiss_input_param_form(self):
        self.browser.find_element_by_id("input_param_cancel").click()

    def reach_add_action_page(self, integration_data_file, integration_name):
        integration_data = json.loads(open(self.test_data_directory + integration_data_file).read())
        integration = Integration(**integration_data)

        with mock.patch('integrator.views.ui.integration.views.Integration') as integration_mock:
            with mock.patch('integrator.views.ui.action.views.Integration') as action_integration_mock:
                integration_mock.objects.all = mock.Mock()
                integration_mock.objects.get = mock.Mock()
                conf = {'return_value': [integration]}
                integration_mock.objects.all.configure_mock(**conf)
                conf = {'return_value': integration}
                integration_mock.objects.get.configure_mock(**conf)
               
                action_integration_mock.objects.get = mock.Mock()
                conf = {'return_value': integration}
                action_integration_mock.objects.get.configure_mock(**conf)
                
                self.browser.get(self.live_server_url + '/')
                integration_list_element = self.browser.find_element_by_id(integration_name)
                integration_list_element.click()
                self.browser.find_element_by_id('actions_helpscout').click()
                self.browser.find_element_by_id('add_action').click()

    def click_add_action(self, integration_data_file):
        integration_data = json.loads(open(self.test_data_directory + 'helpscout_integration_form.json').read())
        integration = Integration(**integration_data)
        with mock.patch('integrator.views.ui.action.views.Integration') as action_integration_mock:
            action_integration_mock.objects.get = mock.Mock()
            conf = {'return_value': integration}
            action_integration_mock.objects.get.configure_mock(**conf)
            self.browser.find_element_by_id("add_action").click()

    def bring_up_input_param_form(self):
        input_param_form = self.browser.find_elements_by_css_selector('#action_input_params .add_modal_field')[0]
        input_param_form.click()

    def populate_and_submit_input_param_form(self, data_file):
        self.json_to_input_param_form(self.test_data_directory + data_file)
        self.browser.find_element_by_id('input_param_submit').click()

    def bring_up_editing_input_param(self, element_name):
        input_param_list_element = self.browser.find_element_by_id('list_' + element_name)
        input_param_list_element.find_elements_by_css_selector(".edit_field")[0].click()

    def delete_input_param(self, element_name):
        input_param_list_element = self.browser.find_element_by_id('list_' + element_name)
        input_param_list_element.find_elements_by_css_selector(".delete_field")[0].click()

    def get_input_params(self):
        input_params = self.browser.find_element_by_id('action_input_params')
        input_params = input_params.find_elements_by_css_selector("li")
        return input_params

    def verify_input_param_order(self, input_param_list):
        input_params = self.get_input_params()
        self.assertEquals(len(input_params), len(input_param_list))
        for index, value in enumerate(input_param_list):
            self.assertEquals(input_params[index].text, value + ' - Edit/Delete')

    def assert_proper_form_structure(self):
        add_action_form = self.browser.find_element_by_id('add_action_form')
        number_of_form_elements = len(add_action_form.find_elements_by_css_selector(".form-group"))
        self.assertEquals(13, number_of_form_elements)

    def test_form_structure(self):
        self.reach_add_action_page('helpscout_integration_form.json', 'helpscout')
        self.assert_proper_form_structure()
        
    def test_if_input_params_are_added_alphabetically(self):
        self.reach_add_action_page('helpscout_integration_form.json', 'helpscout')
        self.bring_up_input_param_form()
        self.populate_and_submit_input_param_form('subject_input_param.json')
        self.bring_up_input_param_form()
        self.populate_and_submit_input_param_form('body_input_param.json')
        input_params = ['body', 'subject']
        self.verify_input_param_order(input_params)
        
    def test_if_input_param_form_resets_after_usage(self):
        self.reach_add_action_page('helpscout_integration_form.json', 'helpscout')
        self.bring_up_input_param_form()
        self.populate_and_submit_input_param_form('subject_input_param.json')
        self.bring_up_input_param_form()

        self.assert_form_is_free_of_errors('input_param_form')
        input_param_data = self.input_param_form_to_json()
        expected_data = json.loads(open(self.test_data_directory + 'default_empty_input_param.json').read())

        self.assertEquals(input_param_data, expected_data)

    def test_if_input_param_form_resets_after_partial_usage(self):
        self.reach_add_action_page('helpscout_integration_form.json', 'helpscout')
        self.bring_up_input_param_form()
        self.populate_and_submit_input_param_form('without_mandatory_input_param.json')
        self.dismiss_input_param_form()
        self.bring_up_input_param_form()

        self.assert_form_is_free_of_errors('input_param_form')
        
        input_param_data = self.input_param_form_to_json()
        expected_data = json.loads(open(self.test_data_directory + 'default_empty_input_param.json').read())
        self.assertEquals(input_param_data, expected_data)

    def test_if_edit_input_param_will_display_right_values(self):
        self.reach_add_action_page('helpscout_integration_form.json', 'helpscout')
        self.bring_up_input_param_form()
        self.populate_and_submit_input_param_form('subject_input_param.json')

        self.bring_up_editing_input_param('subject')
        self.assert_form_is_free_of_errors('input_param_form')
        input_param_data = self.input_param_form_to_json()
        expected_data = json.loads(open(self.test_data_directory + 'subject_input_param.json').read())
        self.assertEquals(input_param_data, expected_data)


    def test_if_edit_input_param_changes_key(self):
        self.reach_add_action_page('helpscout_integration_form.json', 'helpscout')
        self.bring_up_input_param_form()
        self.populate_and_submit_input_param_form('subject_input_param.json')
        self.bring_up_editing_input_param('subject')
        self.clear_input_param_form()

        self.populate_and_submit_input_param_form('body_input_param.json')
        self.bring_up_editing_input_param('body')

        input_param_data = self.input_param_form_to_json()
        expected_data = json.loads(open(self.test_data_directory + 'body_input_param.json').read())

        try:
            self.browser.find_element_by_id('list_subject')
            self.fail("list_subject field still exists")
        except NoSuchElementException:
            pass

        self.assertEquals(input_param_data, expected_data)

    def test_delete_input_params(self):
        self.reach_add_action_page('helpscout_integration_form.json', 'helpscout')
        self.bring_up_input_param_form()
        self.populate_and_submit_input_param_form('subject_input_param.json')
        self.bring_up_input_param_form()
        self.populate_and_submit_input_param_form('body_input_param.json')
        self.bring_up_input_param_form()
        self.populate_and_submit_input_param_form('mailbox_input_param.json')
        input_params = ['body', 'mailbox', 'subject']
        self.verify_input_param_order(input_params)


        self.delete_input_param('mailbox')
        input_params = ['body', 'subject']
        self.verify_input_param_order(input_params)

        self.delete_input_param('body')
        input_params = ['subject']
        self.verify_input_param_order(input_params)

        self.delete_input_param('subject')
        input_params = []
        self.verify_input_param_order(input_params)

    def test_submission_of_duplicate_input_param_key(self):
        self.reach_add_action_page('helpscout_integration_form.json', 'helpscout')
        self.bring_up_input_param_form()
        self.populate_and_submit_input_param_form('subject_input_param.json')
        self.bring_up_input_param_form()
        self.populate_and_submit_input_param_form('subject_input_param.json')

        self.assert_form_error_for_field('key', 'key name subject already exists')
        

    def test_if_mandatory_fields_are_asked_for(self):
        self.reach_add_action_page('helpscout_integration_form.json', 'helpscout')
        self.click_add_action('helpscout_integration_form.json')

        self.assert_form_error_for_mandatory_field('name')
        self.assert_form_error_for_mandatory_field('display')
        self.assert_form_error_for_mandatory_field('description')

    def test_action_form_validation_for_api_type(self):
        self.reach_add_action_page('helpscout_integration_form.json', 'helpscout')

        self.make_selection("api_type", "SOAP")

        self.click_add_action('helpscout_integration_form.json')

        self.assert_form_error_for_field('api_type', 'Please choose a valid api type.')

        self.make_selection("api_type", "----")
        self.click_add_action('helpscout_integration_form.json')

        self.assert_form_error_for_field('api_type', 'Please choose a valid api type.')

        self.make_selection("api_type", "OAuth Workflow")
        self.click_add_action('helpscout_integration_form.json')

        self.assert_form_error_for_field('api_type', 'Please choose a valid api type.')

    def test_wrong_data_submission(self):
        self.reach_add_action_page('helpscout_integration_form.json', 'helpscout')

        self.make_selection("api_type", "REST")
        self.json_to_action_form(self.test_data_directory + 'wrong_data_action_form.json')

        self.click_add_action('helpscout_integration_form.json')

        self.assert_form_error_for_mandatory_field('description')
        self.assert_form_error_for_mandatory_field('display')
        self.assert_form_error_for_field('http_url', 'This doesn\'t look like a url even after translating syntax')
        self.assert_form_error_for_field('name', 'Please use characters A-Z, a-z, 0-9 or _ to create a name and maximum length 20')
        self.assert_form_error_for_field('basic_auth', 'Please use the suggested syntax')
        self.assert_form_error_for_field('http_request_params', 'Please use the suggested syntax')
        self.assert_form_error_for_field('success_response', 'Please use a valid response code')

    def test_success_case_of_action_submission(self):
        self.reach_add_action_page('helpscout_integration_form.json', 'helpscout')
        self.make_selection("api_type", "REST")
        self.json_to_action_form(self.test_data_directory + 'success_case_action_form.json')

        with mock.patch.object(Action, 'save', side_effect=None):
            self.click_add_action('helpscout_integration_form.json')
        
        alert = self.browser.find_element_by_id("notification_window")
        self.assertIn("Action added successfully", alert.text)

    def test_submission_of_duplicate_name(self):
        self.reach_add_action_page('helpscout_integration_form.json', 'helpscout')
        self.make_selection("api_type", "REST")
        self.json_to_action_form(self.test_data_directory + 'success_case_action_form.json')

        with mock.patch.object(Action, 'save', side_effect=NotUniqueError):
            self.click_add_action('helpscout_integration_form.json')
        
        self.assert_form_error_for_field('name', 'Action with name create_ticket already exists')



