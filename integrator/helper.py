from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from models import AUTH_CHOICES, AUTH_SOURCE_CHOICES, FIELD_TYPE_CHOICES
import string

MANDATORY_FORM_FIELDS = ('name', 'display_name', 'description', 'logo_url', 'icon_url')
URL_FIELDS = ('logo_url', 'icon_url', 'auth_validation_endpoint', 'contact_synchronisation_endpoint',
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
