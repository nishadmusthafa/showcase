from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from integrator.syntax import SpecialSyntaxTranslator
from integrator.views.generic import JSONView
import json
import requests
import logging


class Bridge(object):
    def __init__(self):
        self.logger = logging.getLogger('django')
        self.translator = SpecialSyntaxTranslator()

    def relay_request(self):
        # Unimplemented as it is dependent on
        # protocol
        pass

    def prepare_data(self):
        self.translation_input = {}
        self.translation_output = {}
        self.context = {}
        if self.direction == "forward":
            self.prepare_forward_translation_input()
            self.prepare_forward_context()
        else:
            self.prepare_backward_translation_input()
            self.prepare_backward_context()

        self.translate()

    def translate_forward(self):
        self.direction = "forward"
        self.prepare_data()

    def translate(self):
        for key in self.translation_input:
            self.translate_input(key)

    def translate_input(self, key):
        self.translator.set_input(self.translation_input[key])
        self.translator.translate_special_syntax()
        self.translation_output[key] = self.translator.output

    def translate_return(self):
        self.direction = "backward"
        self.prepare_data()

    def handle_request(self, request, *args, **kwargs):
        self.translate_forward()
        self.relay_request()
        self.translate_return()

class JSONRestBridge(Bridge):
    def relay_request(self):
        http_request = {'url': self.translation_output['http_url'],
                        'method': self.translation_output['http_method']
                        }
        if http_request['method'] == 'post':
            http_request['data'] = self.translation_output['payload']
        elif http_request['method'] == 'get':
            http_request['params'] = self.translation_output['payload']
        http_request['headers'] = {'Content-type': 'application/json'}
        if self.translation_output['basic_auth']:
            http_request['auth'] = tuple(self.translation_output['basic_auth'].split(':'))

        self.logger.info("External service request %s" % http_request)
        self.interim_result = requests.request(**http_request)
        self.logger.info("External service response code:%s "
                         "content:%s" % (self.interim_result.status_code, self.interim_result.content))


    def prepare_forward_translation_input(self):
        self.translation_input['http_url'] = self.http_url_stencil()
        self.translation_input['basic_auth'] = self.basic_auth_stencil()
        self.translation_input['payload'] = self.payload_stencil()
        self.translation_input['http_method'] = self.http_method_stencil()

    def prepare_forward_context(self):
        self.translator.build_context(self.inbound_data)

    def handle_request(self, request, *args, **kwargs):
        self.inbound_data = json.loads(request.body)
        super(JSONRestBridge, self).handle_request(request, *args, **kwargs)

    def translate_return(self):
        self.return_context = self.generate_return_context()
        self.response_code = self.generate_return_code()

    def generate_return_context(self):
        return json.loads(self.interim_result.content)

    def generate_return_code(self):
        if self.interim_result.status_code == self.expected_success:
            return self.returned_success
        else:
            return self.returned_failure

class TalkdeskBridgeView(JSONView):
    def __init__(self):
        self.logger = logging.getLogger('django')
        super(TalkdeskBridgeView, self).__init__

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        path = request.META['PATH_INFO']
        self.logger.info("Request on path %s with data %s" % (path, request.body))
        return super(TalkdeskBridgeView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self):
        self.logger.info("Returned result %s" % (self.bridge.return_context))
        return self.bridge.return_context

    def post(self, request, *args, **kwargs):
        self.set_bridge(request, *args, **kwargs)
        self.bridge.handle_request(request, *args, **kwargs)
        context = self.get_context_data()
        response_code = self.bridge.response_code
        return self.render_to_response(context, status=response_code)

    def set_bridge(request, *args, **kwargs):
        self.bridge = JSONRestBridge()