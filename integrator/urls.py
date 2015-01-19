from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import integrator.views

urlpatterns = patterns('',
    url(r'^$', integrator.views.index, name='index'),
    url(r'^integration/$', integrator.views.get_integrations, name='integration'),
    url(r'^integration/create/$', integrator.views.create_integration, name='create_integration'),
    url(r'^integration/create/form/$', integrator.views.create_integration_form, name='create_integration_form'),
)
