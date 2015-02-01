from django.conf import settings
from django.test import TestCase
from django.test.client import Client
from integrator.models import Action
import json
import mock

import logging

logging.disable(logging.CRITICAL)

class ActionEndpointTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_data_directory = getattr(settings, "BASE_DIR") + '/../functional_tests/test_data/'

    def test_verify_params_sent_to_external_service(self):
        action_data_file = 'create_ticket_helpscout_full_action.json'
        action_data = json.loads(open(self.test_data_directory + action_data_file).read())
        action = Action(**action_data)

        payload = {
                        "auth": {
                                    "api_key": "AAA",
                                },
                        "meta": {
                                "contact_external_id": "45880711",
                                "agent_external_id": "2"
                                },
                        "data": {
                                "subject": "Call missed in Talkdesk",
                                "body": "A call from Jane Doe was missed.",
                                "mailbox": "37924"
                                }
                    }
        with mock.patch('integrator.views.endpoints.views.Action') as action_mock:
            action_mock.objects.filter = mock.Mock()
            conf = {'return_value': [action]}
            action_mock.objects.filter.configure_mock(**conf)
            with mock.patch('requests.request') as mock_request:
                response = self.client.post('/integrations/helpscou/actions/create_ticket/', 
                                            content_type='application/json', data=json.dumps(payload))
        
        arg =  {'url': u'https://api.helpscout.net/v1/conversations.json', 'headers': {'Content-type': 'application/json'}, 'data': u'{\n    "customer": {\n        "id": "45880711"\n    },\n    "subject": "Call missed in Talkdesk",\n    "mailbox": {\n        "id": "37924"\n    },\n     "threads": [\n        {\n            "type": "customer",\n            "createdBy": {\n                "id": "45880711",\n                "type": "customer"\n            },\n            "body": "A call from Jane Doe was missed."\n            }\n    ]\n}', 'method': u'post', 'auth': (u'AAA', u'X')}
        mock_request.assert_called_with(**arg)

    def test_non_existent_action(self):
        payload = {
                        "auth": {
                                    "api_key": "AAA",
                                },
                        "meta": {
                                "contact_external_id": "45880711",
                                "agent_external_id": "2"
                                },
                        "data": {
                                "subject": "Call missed in Talkdesk",
                                "body": "A call from Jane Doe was missed.",
                                "mailbox": "37924"
                                }
                    }
        with mock.patch('integrator.views.endpoints.views.Action') as action_mock:
            action_mock.objects.filter = mock.Mock()
            conf = {'side_effect': IndexError}
            action_mock.objects.filter.configure_mock(**conf)
            response = self.client.post('/integrations/helpscou/actions/create_ticket/', 
                                            content_type='application/json', data=json.dumps(payload))

        self.assertEquals(response.status_code, 404)
        response = json.loads(response.content)
        self.assertEquals(response['error'], "Action does not exist")

    def test_verify_params_returned_to_talkdesk_for_correct_external_service_response(self):
        action_data_file = 'create_ticket_helpscout_full_action.json'
        action_data = json.loads(open(self.test_data_directory + action_data_file).read())
        action = Action(**action_data)

        payload = {
                        "auth": {
                                    "api_key": "AAA",
                                },
                        "meta": {
                                "contact_external_id": "45880711",
                                "agent_external_id": "2"
                                },
                        "data": {
                                "subject": "Call missed in Talkdesk",
                                "body": "A call from Jane Doe was missed.",
                                "mailbox": "37924"
                                }
                    }
        with mock.patch('integrator.views.endpoints.views.Action') as action_mock:
            action_mock.objects.filter = mock.Mock()
            conf = {'return_value': [action]}
            action_mock.objects.filter.configure_mock(**conf)
            with mock.patch('requests.request') as mock_request:
                type(mock_request.return_value).status_code = mock.PropertyMock(return_value=201)
                response = self.client.post('/integrations/helpscou/actions/create_ticket/', 
                                            content_type='application/json', data=json.dumps(payload))
        
        self.assertEquals(response.status_code, 201)

    def test_verify_params_returned_to_talkdesk_for_incorrect_external_service_response(self):
        action_data_file = 'create_ticket_helpscout_full_action.json'
        action_data = json.loads(open(self.test_data_directory + action_data_file).read())
        action = Action(**action_data)

        payload = {
                        "auth": {
                                    "api_key": "AAA",
                                },
                        "meta": {
                                "contact_external_id": "45880711",
                                "agent_external_id": "2"
                                },
                        "data": {
                                "subject": "Call missed in Talkdesk",
                                "body": "A call from Jane Doe was missed.",
                                "mailbox": "37924"
                                }
                    }
        with mock.patch('integrator.views.endpoints.views.Action') as action_mock:
            action_mock.objects.filter = mock.Mock()
            conf = {'return_value': [action]}
            action_mock.objects.filter.configure_mock(**conf)
            with mock.patch('requests.request') as mock_request:
                type(mock_request.return_value).status_code = mock.PropertyMock(return_value=400)
                response = self.client.post('/integrations/helpscou/actions/create_ticket/', 
                                            content_type='application/json', data=json.dumps(payload))
        
        self.assertEquals(response.status_code, 400)


