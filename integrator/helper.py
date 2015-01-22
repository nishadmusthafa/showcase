from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from models import AUTH_CHOICES, AUTH_SOURCE_CHOICES, FIELD_TYPE_CHOICES
import string
import re

MANDATORY_FORM_FIELDS = ('name', 'display_name', 'description', 'logo_url', 'icon_url')
URL_FIELDS = ('logo_url', 'icon_url', 'auth_validation_endpoint', 'contact_synchronization_endpoint',
              'interaction_retrieval_endpoint')

def validate_integration_form_data(integration_data):
    errors = {}
    valid = True
    for field in MANDATORY_FORM_FIELDS:
        value = integration_data.get(field, '')
        # Text boxes can give a longer whitespace. 
        # The below condition detects that.
        if all(c in string.whitespace for c in value):
            valid = False
            errors[field] = field + " is mandatory"
    authentication_type = integration_data.get('authentication_type', 'none')
    auth_fields = integration_data.get('auth_field_list', [])

    pattern = re.compile("^[A-Za-z0-9_]+$")
    if 'name' not in errors and not pattern.match(integration_data.get('name', "")):
        valid = False
        errors['name'] = "Please use characters A-Z, a-z, 0-9 or _ to create a name"

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

def serialize_integration(integration):
    auth_conf_list = []
    for auth_conf in integration.authentication_configuration:
        auth_conf_item = {}
        auth_conf_item['source'] = auth_conf.source
        auth_conf_item['display'] = auth_conf.display
        auth_conf_item['type'] = auth_conf.field_type
        auth_conf_item['format'] = auth_conf.field_format
        auth_conf_item['help'] = auth_conf.help_text
        auth_conf_item['store'] = auth_conf.store
        auth_conf_item['mandatory'] = auth_conf.mandatory
        auth_conf_list.append({
                                auth_conf.element: auth_conf_item
                              })

    serialized_integration = {}
    serialized_integration['name'] = integration.name
    serialized_integration['display_name'] = integration.display_name
    serialized_integration['description'] = integration.description
    serialized_integration['logo_url'] = integration.logo_url
    serialized_integration['icon_url'] = integration.icon_url
    serialized_integration['authentication_type'] = integration.authentication_type
    serialized_integration['authentication_configuration'] = auth_conf_list
    serialized_integration['auth_validation_endpoint'] = integration.auth_validation_endpoint
    serialized_integration['contact_synchronization_endpoint'] = integration.contact_synchronization_endpoint
    serialized_integration['interaction_retrieval_endpoint'] = integration.interaction_retrieval_endpoint
    serialized_integration['interaction_types'] = integration.interaction_types

    return serialized_integration




