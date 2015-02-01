from django.conf import settings
from django.test import TestCase
from django.test.client import Client
from integrator.models import ActionInputParam, Action
import json
import mock

import logging

logging.disable(logging.CRITICAL)

class ActionJSONTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_data_directory = getattr(settings, "BASE_DIR") + '/../functional_tests/test_data/'

    def test_generation_of_json(self):
        action_data_file = 'create_ticket_action_form.json'
        body_input_param_file = 'body_input_param.json'
        subject_input_param_file = 'subject_input_param.json'
        action_data = json.loads(open(self.test_data_directory + action_data_file).read())
        body_data = json.loads(open(self.test_data_directory + body_input_param_file).read())
        subject_data = json.loads(open(self.test_data_directory + subject_input_param_file).read())
        action = Action(**action_data)
        body_input_param = ActionInputParam(**body_data)
        subject_input_param = ActionInputParam(**subject_data)
        action.inputs.append(body_input_param)
        action.inputs.append(subject_input_param)
        with mock.patch('integrator.views.configuration_json.views.Action') as action_mock:
            action_mock.objects.get = mock.Mock()
            conf = {'return_value': action}
            action_mock.objects.get.configure_mock(**conf)
            response = self.client.get('/integration/helpscout/action/create_ticket/json/', SERVER_NAME="talkdesk-integrator.com")

        response = json.loads(response.content)
        self.assertTrue('inputs' in response)
        self.assertEquals(2, len(response['inputs']))
        for input_data in response['inputs']:
            self.assertIn(input_data, [subject_data, body_data])

        self.assertEquals(response["endpoint"],
                          "http://talkdesk-integrator.com/integrations/helpscout/actions/create_ticket/")

        for key in action_data.keys():
            self.assertEquals(response[key], action_data[key])








