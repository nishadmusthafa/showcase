from django.http import Http404
from bridge import JSONRestBridge, TalkdeskBridgeView
from datetime import datetime
from integrator.models import Action
import json
import pytz

class ActionBridge(JSONRestBridge):
    def __init__(self, integration_id, action_id):
        super(ActionBridge, self).__init__()
        try:
            self.action = Action.objects.filter(provider=integration_id, name=action_id)[0]
        except IndexError:
            self.action = None
            return
        self.expected_success = int(self.action.external_request['success_response'])
        self.returned_success = 201
        self.returned_failure = 400

    def http_url_stencil(self):
        return self.action.external_request['http_url']

    def http_method_stencil(self):
        return self.action.external_request['http_method']

    def basic_auth_stencil(self):
        return self.action.external_request['basic_auth']

    def payload_stencil(self):
        return self.action.external_request['request_params']

    def translate_input(self, key):
        if key == 'payload':
            self.translator.set_input(self.translation_input[key])
            self.translator.enquote_strings()
            self.translator.translate_special_syntax()
            self.translation_output[key] = self.translator.output
            self.translator.unenquote_strings()
        else:
            super(ActionBridge, self).translate_input(key)

    def generate_return_context(self):
        return {}

    def handle_request(self, request, *args, **kwargs):
        if not self.action:
            self.response_code = 404
            self.return_context = {'error': 'Action does not exist'}
            return
        super(ActionBridge, self).handle_request(request, *args, **kwargs)

class ActionBridgeView(TalkdeskBridgeView):
    def set_bridge(self, request, *args, **kwargs):
        # In later iterations we can build a SOAP bridge if
        # the external API is a SOAP API. At this point, 
        # the implementation is limited to JSON based Rest API
        self.bridge = ActionBridge(kwargs['integration_id'], kwargs['action_id'])


############################################################
# I have created UI views for configuring Integration and  #
# actions. For the remaining, I am hardcoding the stencil  #
# data. My apologies for this. I am a little hard pressed  #
# on time to complete all the views. My main intention was #
# to show a prototype for Action and Integration           #
############################################################
class AuthBridge(JSONRestBridge):
    def __init__(self):
        super(AuthBridge, self).__init__()
        self.expected_success = 200
        self.returned_success = 204
        self.returned_failure = 401

    def http_url_stencil(self):
        return 'https://api.helpscout.net/v1/mailboxes.json'

    def http_method_stencil(self):
        return 'get'

    def basic_auth_stencil(self):
        return '%auth.api_key%:X'

    def payload_stencil(self):
        return '{}'

    def translate_input(self, key):
        super(AuthBridge, self).translate_input(key)

    def generate_return_context(self):
        return {}

class AuthView(TalkdeskBridgeView):
    def set_bridge(self, request, *args, **kwargs):
        self.bridge = AuthBridge()


class ContactBridge(JSONRestBridge):
    def __init__(self):
        super(ContactBridge, self).__init__()
        self.expected_success = 200
        self.returned_success = 200
        self.returned_failure = 400

    def http_url_stencil(self):
        return 'https://api.helpscout.net/v1/customers.json'

    def basic_auth_stencil(self):
        return '%auth.api_key%:X'

    def http_method_stencil(self):
        return 'get'

    def payload_stencil(self):
        payload = {}
        if 'meta' in self.inbound_data:
            if 'synchronization_checkpoint' in self.inbound_data['meta']:
                payload['modifiedSince'] = "%meta.synchronization_checkpoint%"
            payload['page'] = "%meta.offset%" if 'offset' in self.inbound_data['meta'] else "1"
        return json.dumps(payload)

    def generate_return_context(self):
        context = {}
        interim_result = json.loads(self.interim_result.content)
        if not interim_result['pages'] == 0 and not interim_result['page'] == interim_result['pages']:
            context['next_offset'] = str(int(interim_result['page']) + 1)

        contacts = []
        for item in interim_result['items']:
            contacts.append({'name': item['fullName'], 'id': str(item['id'])})
        context['contacts'] = contacts
        context['synchronization_checkpoint'] = \
        datetime.utcnow().replace(tzinfo=pytz.utc).strftime("%Y-%m-%d %H:%M:%S %Z")
        return context

    def translate_input(self, key):
        if key == 'payload':
            self.translator.set_input(self.translation_input[key])
            self.translator.translate_special_syntax()
            temp_output = json.loads(self.translator.output)
            # Limitation here. We are forced to consider the timezone as UTC
            if 'modifiedSince' in temp_output:
                modified_since = datetime.strptime(temp_output['modifiedSince'], "%Y-%m-%d %H:%M:%S %Z")
                temp_output['modifiedSince'] = modified_since.strftime("%Y-%m-%dT%H:%M:%SZ")
            self.translation_output[key] = temp_output
        else:
            super(ContactBridge, self).translate_input(key)


class ContactView(TalkdeskBridgeView):
    def set_bridge(self, request, *args, **kwargs):
        self.bridge = ContactBridge()

class AgentBridge(JSONRestBridge):
    def __init__(self):
        super(AgentBridge, self).__init__()
        self.expected_success = 200
        self.returned_success = 200
        self.returned_failure = 400

    def http_url_stencil(self):
        return 'https://api.helpscout.net/v1/users/me.json'

    def basic_auth_stencil(self):
        return '%auth.api_key%:X'

    def http_method_stencil(self):
        return 'get'

    def payload_stencil(self):
        return '{}'

    def generate_return_context(self):
        interim_result = json.loads(self.interim_result.content)['item']
        context = {
                    "agents" : [ 
                                    {
                                        'id': interim_result['id'],
                                        'name': interim_result['fullName'],
                                        'email': interim_result['email']
                                    }
                                ]
                    }           
        return context

class AgentView(TalkdeskBridgeView):
    def set_bridge(self, request, *args, **kwargs):
        self.bridge = AgentBridge()

# Choosing not to implement this in this iteration. It 
# will now return an empty set
class InteractionBridge(JSONRestBridge):
    def handle_request(self, request, *args, **kwargs):
        self.response_code = 200
        self.return_context = []

class InteractionView(TalkdeskBridgeView):
    def set_bridge(self, request, *args, **kwargs):
        self.bridge = InteractionBridge()


