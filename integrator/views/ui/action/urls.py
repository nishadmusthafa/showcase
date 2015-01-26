from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
        url(r'^integration/(?P<integration_id>\w+)/action/$', 
        views.get_integration_actions, 
        name='integration_actions'),
    url(r'^integration/(?P<integration_id>\w+)/add/action/form/$', 
        views.add_action_form,
        name='add_action_form'),
    url(r'^integration/(?P<integration_id>\w+)/action/add/$',
        views.add_action, name='add_action'),
    url(r'^integration/(?P<integration_id>\w+)/action/(?P<action_id>\w+)/$', 
        views.action_detail, name='action_detail'),
)
