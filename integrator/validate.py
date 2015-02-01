from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from syntax import SpecialSyntaxTranslator
from models import AUTH_CHOICES, AUTH_SOURCE_CHOICES, FIELD_TYPE_CHOICES
import json
import string
import re

MANDATORY_INTEGRATION_FORM_FIELDS = ('name', 'display_name', 'description', 'logo_url', 'icon_url')
URL_FIELDS = ('logo_url', 'icon_url', 'auth_validation_endpoint', 'contact_synchronization_endpoint',
              'interaction_retrieval_endpoint')
MANDATORY_ACTION_FORM_FIELDS = ('name', 'display', 'description')


def validate_integration_form_data(integration_data):
    errors = {}
    valid = True
    for field in MANDATORY_INTEGRATION_FORM_FIELDS:
        value = integration_data.get(field, '')
        # The below condition detects only whitespace
        if all(c in string.whitespace for c in value):
            valid = False
            errors[field] = field + " is mandatory"
    authentication_type = integration_data.get('authentication_type', 'none')
    auth_fields = integration_data.get('auth_field_list', [])

    pattern = re.compile("^[A-Za-z0-9_]{1,20}$")
    if 'name' not in errors and not pattern.match(integration_data.get('name', "")):
        valid = False
        errors['name'] = "Please use characters A-Z, a-z, 0-9 or _ to create a name and maximum length 20"

    if authentication_type not in zip(*AUTH_CHOICES)[0]:
        valid = False
        errors['authentication_type'] = 'Valid auth types are ' + ", ".join(zip(*AUTH_CHOICES)[0])

    if authentication_type == "custom" and not auth_fields:
        valid = False
        errors['auth_field_list'] = 'Auth Fields are mandatory for custom authentication type'

    for url_field in URL_FIELDS:
        if url_field in integration_data and url_field not in errors:
            if all(c in string.whitespace for c in integration_data[url_field]):
                continue
            validate = URLValidator()
            try:
                validate(integration_data[url_field])
            except ValidationError, e:
                valid = False
                errors[url_field] = "Please key in a valid url"

    return valid, errors

def validate_action_form_data(action_data):
    errors = {}
    valid = True
    for field in MANDATORY_ACTION_FORM_FIELDS:
        value = action_data.get(field, '')
        if all(c in string.whitespace for c in value):
            valid = False
            errors[field] = field + " is mandatory"

    pattern = re.compile("^[A-Za-z0-9_]{1,20}$")
    if 'name' not in errors and not pattern.match(action_data.get('name', "")):
        valid = False
        errors['name'] = "Please use characters A-Z, a-z, 0-9 or _ to create a name and maximum length 20"

    external_request = action_data.get('external_request', {})
    api_type = external_request.get('type', 'none')

    if api_type not in ['oauth', 'soap', 'rest']:
        errors['api_type'] = 'Please choose a valid api type.'
        valid = False
    elif api_type not in ['rest']:
        errors['api_type'] = 'Please choose an api type that is supported now'
        valid = False
    else:
        request_specific_validator = get_request_specific_validator(api_type)
        valid, request_errors = request_specific_validator(external_request)
        errors.update(request_errors)

    return valid, errors

def rest_request_validator(external_request):
    errors = {}
    valid = True
    http_url = external_request.get('http_url', '')
    http_method = external_request.get('http_method', '')
    basic_auth = external_request.get('basic_auth', '')
    success_response = external_request.get('success_response', '')
    request_params = external_request.get('request_params', '')

    if http_method not in ['get', 'post']:
        valid = False
        errors['http_method'] = 'Please use GET or POST'

    unflat_context = {"*": "generic_string1234"}
    translator = SpecialSyntaxTranslator()
    translator.build_context(unflat_context)

    translator.set_input(http_url)
    translator.translate_special_syntax()
    http_url = translator.output

    translator.set_input(basic_auth)
    translator.translate_special_syntax()
    basic_auth = translator.output

    translator.set_input(request_params)
    translator.enquote_strings()
    translator.translate_special_syntax()
    request_params = translator.output

    validate = URLValidator()
    try:
        validate(http_url)
    except ValidationError, e:
        valid = False
        errors['http_url'] = "This doesn't look like a url even after translating syntax"

    if basic_auth is not "" and not ":" in basic_auth:
        valid = False
        errors['basic_auth'] = "Please use the suggested syntax"

    if not success_response.isdigit():
        valid = False
        errors['success_response'] = "Please use a valid response code"

    try:
        request_params = json.loads(request_params)
    except ValueError:
        valid = False
        errors['http_request_params'] = "Please use the suggested syntax"

    return valid, errors

def get_request_specific_validator(api_type):
    if api_type == 'rest':
        return rest_request_validator
    # More will be added as they get supported
    return None
