from django.conf.urls import patterns, include, url
from views import get_action_json, get_integration_json

urlpatterns = patterns('',
    url(r'^integration/(?P<integration_id>\w+)/json/$',
        get_integration_json,
        name='integration_json'),
    url(r'^integration/(?P<integration_id>\w+)/action/(?P<action_id>\w+)/json/$',
        get_action_json,
        name='integration_json'),
)
