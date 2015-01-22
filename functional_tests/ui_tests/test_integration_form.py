from functional_tests.test_utils.helper import UITestCase
from integrator.models import Integration
from selenium.common.exceptions import NoSuchElementException
import json
import mock
from mongoengine.errors import NotUniqueError


class IntegrationFormTest(UITestCase):
    def json_to_auth_form(self, data_file_path):
        auth_field_data = json.loads(open(data_file_path).read())
        self.key_in_input("element", auth_field_data.get("element", ""))
        self.key_in_input("display", auth_field_data.get("display", ""))
        self.key_in_input("help_text", auth_field_data.get("help_text", ""))
        self.make_selection("source", auth_field_data.get("source", "Input"))
        self.make_selection("field_type", auth_field_data.get("field_type", "Input"))
        if auth_field_data["store"]:
            self.check_check_box("store")
        else:
            self.uncheck_check_box("store")
        if auth_field_data["mandatory"]:
            self.check_check_box("mandatory")
        else:
            self.uncheck_check_box("mandatory")

    def json_to_integration_form(self, data_file_path):
        integration_form_data = json.loads(open(data_file_path).read())
        self.key_in_input("name", integration_form_data.get("name", ""))
        self.key_in_input("display_name", integration_form_data.get("display_name", ""))
        self.key_in_input("icon_url", integration_form_data.get("icon_url", ""))
        self.key_in_input("logo_url", integration_form_data.get("logo_url", ""))
        self.key_in_input("description", integration_form_data.get("description", ""))
        self.make_selection("authentication_type", integration_form_data.get("authentication_type", "None"))
        self.key_in_input("auth_validation_endpoint", integration_form_data.get("auth_validation_endpoint", ""))
        self.key_in_input("contact_synchronization_endpoint", integration_form_data.get("contact_synchronization_endpoint", ""))
        self.key_in_input("interaction_retrieval_endpoint", integration_form_data.get("interaction_retrieval_endpoint", ""))


    def clear_auth_form(self):
        self.browser.find_element_by_id('element').clear()
        self.browser.find_element_by_id('display').clear()
        self.browser.find_element_by_id('help_text').clear()
        self.uncheck_check_box("mandatory")
        self.uncheck_check_box("store")

    def auth_form_to_json(self):
        auth_form_data = {
                    "element": self.browser.find_element_by_id('element').get_attribute('value'),
                    "display": self.browser.find_element_by_id('display').get_attribute('value'),
                    "help_text": self.browser.find_element_by_id('help_text').get_attribute('value'),
                    "source": self.get_selected_item_in_dropdown('source').get_attribute('text'),
                    "field_type": self.get_selected_item_in_dropdown('field_type').get_attribute('text'),
                    "store": self.browser.find_element_by_id('store').get_attribute("checked") == "true",
                    "mandatory": self.browser.find_element_by_id('mandatory').get_attribute("checked") == "true"
                }
        return auth_form_data

    def reach_add_integration_page(self):
        self.browser.get(self.live_server_url + '/')
        self.wait_till_element_is_clickable('add_integration')
        add_integration = self.browser.find_element_by_id('add_integration')
        add_integration.click()

    def bring_up_adding_auth_field_form(self):
        add_auth_field = self.browser.find_element_by_id('add_auth_field')
        add_auth_field.click()

    def populate_and_submit_add_auth_field_form(self, data_file):
        self.json_to_auth_form(self.test_data_directory + data_file)
        auth_field_form_submit = self.browser.find_element_by_id('auth_field_form_submit')
        auth_field_form_submit.click()

    def bring_up_editing_auth_field_form(self, element_name):
        auth_field_list_element = self.browser.find_element_by_id('list_' + element_name)
        edit_button = auth_field_list_element.find_elements_by_css_selector(".edit_auth_field")[0]
        edit_button.click()

    def delete_auth_field(self, element_name):
        auth_field_list_element = self.browser.find_element_by_id('list_' + element_name)
        delete_button = auth_field_list_element.find_elements_by_css_selector(".delete_auth_field")[0]
        delete_button.click()

    def get_auth_field_list_elements(self):
        auth_field_list = self.browser.find_element_by_id('auth_field_list')
        auth_field_list_elements = auth_field_list.find_elements_by_css_selector("li")
        return auth_field_list_elements

    def verify_auth_field_list_order(self, auth_field_names):
        auth_field_list_elements = self.get_auth_field_list_elements()
        self.assertEquals(len(auth_field_names), len(auth_field_list_elements))
        for index, value in enumerate(auth_field_names):
            self.assertEquals(auth_field_list_elements[index].text, value + ' - Edit/Delete')

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
        help_block = self.find_help_block(id)
        self.assertEquals(help_block.text, "Please key in a valid url")
        form_group = self.find_form_group(id)
        self.assertIn('has-error', form_group.get_attribute('class'))

    def assert_form_error_for_mandatory_field(self, id):
        help_block = self.find_help_block(id)
        self.assertEquals(help_block.text, id + " is mandatory")
        form_group = self.find_form_group(id)
        self.assertIn('has-error', form_group.get_attribute('class'))

    def assert_form_is_free_of_errors(self, form):
        form = self.browser.find_element_by_id(form)
        form_groups = form.find_elements_by_css_selector('form-group')
        for form_group in form_groups:
            self.assertNotIn('has-error', form_group.get_attribute('class'))

    def assert_proper_form_structure(self):
        add_integration_form = self.browser.find_element_by_id('create_integration_form')
        number_of_form_elements = len(add_integration_form.find_elements_by_css_selector(".form-group"))
        self.assertEquals(11, number_of_form_elements)

    def test_form_structure(self):
        self.reach_add_integration_page()
        self.assert_proper_form_structure()
        

    def test_if_auth_fields_are_added_alphabetically(self):
        self.reach_add_integration_page()
        self.bring_up_adding_auth_field_form()
        self.populate_and_submit_add_auth_field_form('api_key_auth_field.json')
        self.bring_up_adding_auth_field_form()
        self.populate_and_submit_add_auth_field_form('account_auth_field.json')
        auth_field_names = ['Account', 'API KEY']
        self.verify_auth_field_list_order(auth_field_names)
        
    def test_if_add_auth_field_form_resets_after_usage(self):
        self.reach_add_integration_page()
        self.bring_up_adding_auth_field_form()
        self.populate_and_submit_add_auth_field_form('api_key_auth_field.json')
        self.bring_up_adding_auth_field_form()

        self.assert_form_is_free_of_errors('auth_field_form')
        auth_form_data = self.auth_form_to_json()
        expected_data = json.loads(open(self.test_data_directory + 'default_empty_auth_field.json').read())

        self.assertEquals(auth_form_data, expected_data)

    def test_if_edit_auth_field_will_display_right_values(self):
        self.reach_add_integration_page()
        self.bring_up_adding_auth_field_form()

        self.assert_form_is_free_of_errors('auth_field_form')
        self.populate_and_submit_add_auth_field_form('account_auth_field.json')
        self.bring_up_editing_auth_field_form('account')

        auth_form_data = self.auth_form_to_json()
        expected_data = json.loads(open(self.test_data_directory + 'account_auth_field.json').read())

        self.assertEquals(auth_form_data, expected_data)

    def test_if_edit_auth_field_functionality_changing_element_name(self):
        self.reach_add_integration_page()
        self.bring_up_adding_auth_field_form()
        self.populate_and_submit_add_auth_field_form('account_auth_field.json')
        self.bring_up_editing_auth_field_form('account')
        self.clear_auth_form()
        self.populate_and_submit_add_auth_field_form('edited_account_auth_field.json')
        self.bring_up_editing_auth_field_form('account_name')

        auth_form_data = self.auth_form_to_json()
        expected_data = json.loads(open(self.test_data_directory + 'edited_account_auth_field.json').read())

        try:
            self.browser.find_element_by_id('list_account')
            self.fail("list_account field still exists")
        except NoSuchElementException:
            pass
        self.assertEquals(auth_form_data, expected_data)

    def test_delete_auth_field_functionality(self):
        self.reach_add_integration_page()
        self.bring_up_adding_auth_field_form()
        self.populate_and_submit_add_auth_field_form('account_auth_field.json')
        self.bring_up_adding_auth_field_form()
        self.populate_and_submit_add_auth_field_form('api_key_auth_field.json')
        self.bring_up_adding_auth_field_form()
        self.populate_and_submit_add_auth_field_form('email_auth_field.json')
        auth_field_names = ['Account', 'API KEY', 'Email']
        self.verify_auth_field_list_order(auth_field_names)


        self.delete_auth_field('api_key')
        auth_field_names = ['Account', 'Email']
        self.verify_auth_field_list_order(auth_field_names)

        self.delete_auth_field('email')
        auth_field_names = ['Account']
        self.verify_auth_field_list_order(auth_field_names)

        self.delete_auth_field('account')
        auth_field_names = []
        self.verify_auth_field_list_order(auth_field_names)

    def test_submission_of_duplicate_name_in_auth_field_form(self):
        self.reach_add_integration_page()
        self.bring_up_adding_auth_field_form()
        self.populate_and_submit_add_auth_field_form('account_auth_field.json')
        self.bring_up_adding_auth_field_form()
        self.populate_and_submit_add_auth_field_form('account_auth_field.json')

        self.assert_form_error_for_field('element', 'Auth Field with element name account already exists')

    def test_submission_without_mandatory_fields_in_auth_field_form(self):
        self.reach_add_integration_page()
        self.bring_up_adding_auth_field_form()
        self.populate_and_submit_add_auth_field_form('without_mandatory_auth_field.json')

        self.assert_form_error_for_mandatory_field('element')
        self.assert_form_error_for_mandatory_field('display')

    def test_if_optional_parameters_give_error_when_not_entered_in_auth_field_form(self):
        self.reach_add_integration_page()
        self.bring_up_adding_auth_field_form()
        self.populate_and_submit_add_auth_field_form('without_optional_auth_field.json')
        auth_field_names = ['Account']
        self.verify_auth_field_list_order(auth_field_names)
        

    def test_if_mandatory_fields_are_asked_for(self):
        self.reach_add_integration_page()
        self.browser.find_element_by_id("create_integration").click()

        self.assert_form_error_for_mandatory_field('name')
        self.assert_form_error_for_mandatory_field('display_name')
        self.assert_form_error_for_mandatory_field('logo_url')
        self.assert_form_error_for_mandatory_field('icon_url')
        self.assert_form_error_for_mandatory_field('description')

    def test_integration_form_validation_for_custom_auth_type(self):
        self.reach_add_integration_page()
    
        self.make_selection("authentication_type", "Custom")
        self.browser.find_element_by_id("create_integration").click()

        self.assert_form_error_for_field('auth_field_list', 'Auth Fields are mandatory for custom authentication type')

    def test_wrong_data_type_submission(self):
        self.reach_add_integration_page()
        self.json_to_integration_form(self.test_data_directory + 'wrong_data_integration_form.json')

        self.browser.find_element_by_id("create_integration").click()

        self.assert_url_validation_error_for_field('logo_url')
        self.assert_url_validation_error_for_field('icon_url')
        self.assert_url_validation_error_for_field('auth_validation_endpoint')
        self.assert_url_validation_error_for_field('contact_synchronization_endpoint')
        self.assert_url_validation_error_for_field('interaction_retrieval_endpoint')
        self.assert_form_error_for_field('name', 'Please use characters A-Z, a-z, 0-9 or _ to create a name')

    def test_if_optional_parameters_do_not_give_error_when_not_entered(self):
        self.reach_add_integration_page()
        self.json_to_integration_form(self.test_data_directory + 'without_optional_integration_form.json')
        
        with mock.patch.object(Integration, 'save', side_effect=None):
            self.browser.find_element_by_id("create_integration").click()
            alert = self.browser.find_element_by_id("notification_window")
            self.assertIn("Integration created successfully", alert.text)

    def test_submission_of_duplicate_name(self):
        self.reach_add_integration_page()
        self.json_to_integration_form(self.test_data_directory + 'without_optional_integration_form.json')

        with mock.patch.object(Integration, 'save', side_effect=NotUniqueError):
            self.browser.find_element_by_id("create_integration").click()

        self.assert_form_error_for_field('name', 'Integration with name helpscout already exists')

    def test_navigation_create_integration_to_index_page(self):
        self.reach_add_integration_page()
        self.json_to_integration_form(self.test_data_directory + 'without_optional_integration_form.json')
        
        with mock.patch.object(Integration, 'save', side_effect=None):
            self.browser.find_element_by_id("create_integration").click()

        self.browser.back()
        self.assert_proper_form_structure()

    def test_load_of_page_by_hash(self):
        self.browser.get(self.live_server_url + '/#create_integration')
        self.assert_proper_form_structure()



