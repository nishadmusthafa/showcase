from django.conf import settings
from django.test import TestCase
from django.test.client import Client
import json
import mock

import logging

logging.disable(logging.CRITICAL)

class AgentEndpointTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_data_directory = getattr(settings, "BASE_DIR") + '/../functional_tests/test_data/'

    def test_verify_params_sent_to_external_service(self):
        payload = {
                "auth": {
                "api_key": "AAA",
                },
                    "meta": {
                     "offset": "2",
                     "synchronization_checkpoint": "2012-11-20 23:01:00 UTC",
                }
                }
        
        with mock.patch('requests.request') as mock_request:
            type(mock_request.return_value).status_code = mock.PropertyMock(return_value=200)
            external_service_return = json.dumps({'item': {'fullName': 'NishadMusthafa', 'email': 'nm@gmail.com', 'id':420}})
            type(mock_request.return_value).content = mock.PropertyMock(return_value=external_service_return)
            response = self.client.post('/integrations/nishadhelpscout/agent_sync/', 
                                        content_type='application/json', data=json.dumps(payload))
    
        arg =  {'url': 'https://api.helpscout.net/v1/users/me.json', 'headers': {'Content-type': 'application/json'}, 'params': '{}', 'method': 'get', 'auth': (u'AAA', u'X')}
        mock_request.assert_called_with(**arg)

    def test_verify_params_returned_to_talkdesk_for_correct_external_service_response(self):
        payload = {
                "auth": {
                "api_key": "AAA",
                },
                    "meta": {
                     "offset": "2",
                     "synchronization_checkpoint": "2012-11-20 23:01:00 UTC",
                }
                }
        
        with mock.patch('requests.request') as mock_request:
            type(mock_request.return_value).status_code = mock.PropertyMock(return_value=200)
            external_service_return = json.dumps({'item': {'fullName': 'Nishad Musthafa', 'email': 'nm@gmail.com', 'id':420}})
            type(mock_request.return_value).content = mock.PropertyMock(return_value=external_service_return)
            response = self.client.post('/integrations/nishadhelpscout/agent_sync/', 
                                        content_type='application/json', data=json.dumps(payload))
    
        self.assertEquals(response.status_code, 200)
        response = json.loads(response.content)
        self.assertIn("agents", response)
        self.assertEquals(len(response['agents']), 1)
        self.assertEquals(response['agents'][0]['id'], 420)
        self.assertEquals(response['agents'][0]['email'], 'nm@gmail.com')
        self.assertEquals(response['agents'][0]['name'], 'Nishad Musthafa')





