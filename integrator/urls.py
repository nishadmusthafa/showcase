from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import integrator.views

urlpatterns = patterns('',
    url(r'^$', integrator.views.index, name='index'),
    url(r'^integration/$', integrator.views.get_integrations, name='integration'),
    url(r'^integration_create/$', integrator.views.create_integration, name='create_integration'),
    url(r'^integration_create/form/$', integrator.views.create_integration_form, name='create_integration_form'),
    url(r'^integration/(?P<integration_id>\w+)/$', integrator.views.get_integration_detail, name='integration_detail'),
    url(r'^integration/(?P<integration_id>\w+)/json/$', integrator.views.get_integration_json, name='integration_json'),
)
