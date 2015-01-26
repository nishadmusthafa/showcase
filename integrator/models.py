from mongoengine import *

AUTH_CHOICES = (
        ('none', u'None'),
        ('custom', u'Custom'),
        ('oauth2', u'OAuth2'),
    )

AUTH_SOURCE_CHOICES = (
        ('input', u'Input'),
        ('default', u'Default'),
        ('auth_validation', u'Auth Validation'),
    )

FIELD_TYPE_CHOICES = (
        ('input', u'Input'),
        ('oauth', u'OAuth'),
    )


class AuthenticationField(EmbeddedDocument):
    element = StringField(max_length=20, required=True)
    source = StringField(choices=AUTH_SOURCE_CHOICES, default="default")
    display = StringField(max_length=20, required=True)
    mandatory = BooleanField(required=True)
    field_type = StringField(choices=FIELD_TYPE_CHOICES, default="default", required=True)
    store = BooleanField(required=True)
    help_text = StringField(max_length=200)
    field_format = StringField(max_length=200)

class Integration(Document):
    name = StringField(max_length=20, unique=True)
    display_name = StringField(max_length=20, required=True)
    description = StringField(max_length=200, required=True)
    logo_url = URLField(required=True)
    icon_url = URLField(required=True)
    authentication_type = StringField(choices=AUTH_CHOICES)
    authentication_configuration = ListField(EmbeddedDocumentField(AuthenticationField))
    interaction_types = ListField(StringField())

    meta = {
        'indexes': [
            'name'
        ]
    }

class ActionInputParam(EmbeddedDocument):
    key = StringField(max_length=20, required=True)
    name = StringField(max_length=20, required=True)
    mandatory = BooleanField(required=True)

class Action(Document):
    name = StringField(max_length=20, unique_with=['provider'])
    provider = StringField(max_length=20, required=True)
    display = StringField(max_length=20, required=True)
    description = StringField(max_length=200, required=True)
    inputs = ListField(EmbeddedDocumentField(ActionInputParam))
    external_request = DictField(required=True)