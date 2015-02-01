from django.conf import settings
from django.test import TestCase
from django.test.client import Client
import json
import mock

import logging

logging.disable(logging.CRITICAL)

class AuthEndpointTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_data_directory = getattr(settings, "BASE_DIR") + '/../functional_tests/test_data/'

    def test_verify_params_sent_to_external_service(self):
        payload = {
                        "auth": {
                                    "api_key": "AAA",
                                }
                    }
        
        with mock.patch('requests.request') as mock_request:
            response = self.client.post('/integrations/nishadhelpscout/auth_validation/', 
                                        content_type='application/json', data=json.dumps(payload))
    
        arg =  {'url': 'https://api.helpscout.net/v1/mailboxes.json', 'headers': {'Content-type': 'application/json'}, 'params': '{}', 'method': 'get', 'auth': (u'AAA', u'X')}
        mock_request.assert_called_with(**arg)

    def test_verify_params_returned_to_talkdesk_for_correct_external_service_response(self):
        payload = {
                        "auth": {
                                    "api_key": "AAA",
                                }
                    }

        with mock.patch('requests.request') as mock_request:
            type(mock_request.return_value).status_code = mock.PropertyMock(return_value=200)
            response = self.client.post('/integrations/nishadhelpscout/auth_validation/', 
                                        content_type='application/json', data=json.dumps(payload))
        
        self.assertEquals(response.status_code, 204)

    def test_verify_params_returned_to_talkdesk_for_incorrect_external_service_response(self):
        payload = {
                        "auth": {
                                    "api_key": "AAA",
                                }
                    }

        with mock.patch('requests.request') as mock_request:
            type(mock_request.return_value).status_code = mock.PropertyMock(return_value=401)
            response = self.client.post('/integrations/nishadhelpscout/auth_validation/', 
                                        content_type='application/json', data=json.dumps(payload))
        
        self.assertEquals(response.status_code, 401)






