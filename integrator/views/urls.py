from django.conf.urls import patterns, include, url
from ui import index

urlpatterns = patterns('',
    url(r'^$', index, name='index'),
    url(r'^', include('integrator.views.ui.urls')),
    url(r'^', include('integrator.views.configuration_json.urls')),
    url(r'^', include('integrator.views.endpoints.urls')),
)
