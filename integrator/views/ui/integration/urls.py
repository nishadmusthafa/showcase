from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^integration/$', 
        views.get_integrations, 
        name='integration'),
    url(r'^integration_create/$', 
        views.create_integration, 
        name='create_integration'),
    url(r'^integration_create/form/$',
        views.create_integration_form,
        name='create_integration_form'),
    url(r'^integration/(?P<integration_id>\w+)/$',
        views.get_integration_detail,
        name='integration_detail'),
)
