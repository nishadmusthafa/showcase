from django.conf import settings
from django.test import TestCase
from django.test.client import Client
from integrator.models import AuthenticationField, Integration
import json
import mock

class IntegrationJSONTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_data_directory = getattr(settings, "BASE_DIR") + '/../functional_tests/test_data/'

    def test_generation_of_json(self):
        integration_data_file = 'helpscout_integration_form.json'
        api_auth_field_file = 'helpscout_api_key_auth_field.json'
        integration_data = json.loads(open(self.test_data_directory + integration_data_file).read())
        auth_field_data = json.loads(open(self.test_data_directory + api_auth_field_file).read())
        integration = Integration(**integration_data)
        auth_conf = AuthenticationField(**auth_field_data)
        integration.authentication_configuration.append(auth_conf)
        with mock.patch('integrator.views.Integration') as integration_mock:
            integration_mock.objects.get = mock.Mock()
            conf = {'return_value': integration}
            integration_mock.objects.get.configure_mock(**conf)
            response = self.client.get('/integration/helpscout/json/')

        response = json.loads(response.content)

        self.assertTrue('api_key' in response['authentication_configuration'][0])
        self.assertEquals(response['authentication_configuration'][0]['api_key']['display'], 
                          auth_field_data['display'])
        self.assertEquals(response['authentication_configuration'][0]['api_key']['source'], 
                          auth_field_data['source'])
        self.assertEquals(response['authentication_configuration'][0]['api_key']['help'], 
                          auth_field_data['help_text'])
        self.assertEquals(response['authentication_configuration'][0]['api_key']['type'], 
                          auth_field_data['field_type'])
        self.assertEquals(response['authentication_configuration'][0]['api_key']['store'], 
                          auth_field_data['store'])
        self.assertEquals(response['authentication_configuration'][0]['api_key']['mandatory'], 
                          auth_field_data['mandatory'])

        for key in integration_data.keys():
            self.assertEquals(response[key], integration_data[key])







