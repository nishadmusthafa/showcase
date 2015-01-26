from django.conf.urls import patterns, include, url

import action, integration

urlpatterns = patterns('',
    url(r'^', include('integrator.views.ui.action.urls')),
    url(r'^', include('integrator.views.ui.integration.urls')),

    # url(r'^integration/$', 
    #     integration.get_integrations, 
    #     name='integration'),
    # url(r'^integration_create/$', 
    #     integration.create_integration, 
    #     name='create_integration'),
    # url(r'^integration_create/form/$',
    #     integration.create_integration_form,
    #     name='create_integration_form'),
    # url(r'^integration/(?P<integration_id>\w+)/$',
    #     integration.get_integration_detail,
    #     name='integration_detail'),
    # url(r'^integration/(?P<integration_id>\w+)/json/$',
    #     ui.integration.get_integration_json,
    #     name='integration_json'),
    
    # url(r'^integration/(?P<integration_id>\w+)/action/$', 
    #     action.get_integration_actions, 
    #     name='integration_actions'),
    # url(r'^integration/(?P<integration_id>\w+)/add/action/form/$', 
    #     action.add_action_form,
    #     name='add_action_form'),
    # url(r'^integration/(?P<integration_id>\w+)/action/add/$',
    #     action.add_action, name='add_action'),
    # url(r'^integration/(?P<integration_id>\w+)/action/(?P<action_id>\w+)/$', 
    #     action.add_action, name='add_action'),
)
