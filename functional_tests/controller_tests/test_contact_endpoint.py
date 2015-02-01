from django.conf import settings
from django.test import TestCase
from django.test.client import Client
import json
import mock

import logging

logging.disable(logging.CRITICAL)

class ContactEndpointTest(TestCase):
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
            external_service_return = json.dumps({'page':1, 'pages':5, 'items': []})
            type(mock_request.return_value).content = mock.PropertyMock(return_value=external_service_return)
            response = self.client.post('/integrations/nishadhelpscout/contact_sync/', 
                                        content_type='application/json', data=json.dumps(payload))
    
        arg =  {'url': 'https://api.helpscout.net/v1/customers.json', 'headers': {'Content-type': 'application/json'}, 'params': {u'modifiedSince': '2012-11-20T23:01:00Z', u'page': u'2'}, 'method': 'get', 'auth': (u'AAA', u'X')}
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
            items = []
            for i in range(20):
                item = {
                            'fullName' : 'Name' + str(i),
                            'id': i,
                            }
                items.append(item)
            external_service_return = json.dumps({'page':2, 'pages':5, 'items': items})
            type(mock_request.return_value).content = mock.PropertyMock(return_value=external_service_return)
            response = self.client.post('/integrations/nishadhelpscout/contact_sync/', 
                                        content_type='application/json', data=json.dumps(payload))
        
        self.assertEquals(response.status_code, 200)
        response = json.loads(response.content)
        self.assertEquals(response['next_offset'], "3")
        self.assertEquals(len(response['contacts']), 20)
        self.assertEquals(response['contacts'][0]['id'], '0')
        self.assertEquals(response['contacts'][0]['name'], 'Name0')

    def test_verify_params_returned_to_talkdesk_for_correct_external_service_response_without_checkpoint(self):
        payload = {
                    "auth": {
                        "api_key": "AAA",
                        },
                            "meta": {
                            "offset": "2",
                        }
                    }

        with mock.patch('requests.request') as mock_request:
            type(mock_request.return_value).status_code = mock.PropertyMock(return_value=200)
            items = []
            for i in range(20):
                item = {
                            'fullName' : 'Name' + str(i),
                            'id': i,
                            }
                items.append(item)
            external_service_return = json.dumps({'page':2, 'pages':5, 'items': items})
            type(mock_request.return_value).content = mock.PropertyMock(return_value=external_service_return)
            response = self.client.post('/integrations/nishadhelpscout/contact_sync/', 
                                        content_type='application/json', data=json.dumps(payload))
        
        self.assertEquals(response.status_code, 200)
        response = json.loads(response.content)
        self.assertEquals(response['next_offset'], "3")
        self.assertEquals(len(response['contacts']), 20)
        self.assertEquals(response['contacts'][0]['id'], '0')
        self.assertEquals(response['contacts'][0]['name'], 'Name0')

    def test_verify_params_returned_to_talkdesk_for_correct_external_service_response_without_offset(self):
        payload = {
                    "auth": {
                        "api_key": "AAA",
                        },
                            "meta": {
                        }
                    }

        with mock.patch('requests.request') as mock_request:
            type(mock_request.return_value).status_code = mock.PropertyMock(return_value=200)
            items = []
            for i in range(20):
                item = {
                            'fullName' : 'Name' + str(i),
                            'id': i,
                            }
                items.append(item)
            external_service_return = json.dumps({'page':1, 'pages':5, 'items': items})
            type(mock_request.return_value).content = mock.PropertyMock(return_value=external_service_return)
            response = self.client.post('/integrations/nishadhelpscout/contact_sync/', 
                                        content_type='application/json', data=json.dumps(payload))
        
        self.assertEquals(response.status_code, 200)
        response = json.loads(response.content)
        self.assertEquals(response['next_offset'], "2")
        self.assertEquals(len(response['contacts']), 20)
        self.assertEquals(response['contacts'][0]['id'], '0')
        self.assertEquals(response['contacts'][0]['name'], 'Name0')

    def test_verify_params_returned_to_talkdesk_for_correct_external_service_response_without_meta(self):
        payload = {
                    "auth": {
                        "api_key": "AAA",
                        },
                    }

        with mock.patch('requests.request') as mock_request:
            type(mock_request.return_value).status_code = mock.PropertyMock(return_value=200)
            items = []
            for i in range(20):
                item = {
                            'fullName' : 'Name' + str(i),
                            'id': i,
                            }
                items.append(item)
            external_service_return = json.dumps({'page':1, 'pages':5, 'items': items})
            type(mock_request.return_value).content = mock.PropertyMock(return_value=external_service_return)
            response = self.client.post('/integrations/nishadhelpscout/contact_sync/', 
                                        content_type='application/json', data=json.dumps(payload))
        
        self.assertEquals(response.status_code, 200)
        response = json.loads(response.content)
        self.assertEquals(response['next_offset'], "2")
        self.assertEquals(len(response['contacts']), 20)
        self.assertEquals(response['contacts'][0]['id'], '0')
        self.assertEquals(response['contacts'][0]['name'], 'Name0')

    def test_verify_params_returned_to_talkdesk_for_no_items_returned(self):
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
            items = []
            external_service_return = json.dumps({'page':1, 'pages':0, 'items': items})
            type(mock_request.return_value).content = mock.PropertyMock(return_value=external_service_return)
            response = self.client.post('/integrations/nishadhelpscout/contact_sync/', 
                                        content_type='application/json', data=json.dumps(payload))
        
        self.assertEquals(response.status_code, 200)
        response = json.loads(response.content)
        self.assertNotIn("next_offset", response)
        self.assertEquals(len(response['contacts']), 0)


        




