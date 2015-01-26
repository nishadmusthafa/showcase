from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from integrator.helper import serialize_integration
from integrator.models import AuthenticationField, Integration
from integrator.validate import validate_integration_form_data
import json
from mongoengine.errors import NotUniqueError


def get_integrations(request):
    integrations = Integration.objects.all()
    context = {'integrations': integrations}
    return render(request, 'integrations.html', context)

def get_integration_detail(request, integration_id):
    try:
        integration = Integration.objects.get(name=integration_id)
    except Integration.DoesNotExist:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    context = {'integration': integration}
    return render(request, 'integration.html', context)

def create_integration_form(request):
    return render(request, 'create_integration_form.html')

def create_integration(request):
    if not request.is_ajax():
        return HttpResponse(status=400)

    integration_data = {}
    for key, value in json.loads(request.body).iteritems():
        if value:
            integration_data[key] = value
    
    is_valid, errors = validate_integration_form_data(integration_data)
    if not is_valid:
        return HttpResponse(content=json.dumps(errors), content_type="application/json", status=400)
    
    auth_field_list = integration_data.get('auth_field_list', {})
    if auth_field_list:
        del(integration_data['auth_field_list'])


    integration = Integration(**integration_data)
    for key, value in auth_field_list.iteritems():
        data = {'element': key}
        data.update(value)
        embedded_auth_field = AuthenticationField(**data)
        integration.authentication_configuration.append(embedded_auth_field)
    
    try:
        integration.save(force_insert=True)
    except NotUniqueError:
        errors = {'name': 'Integration with name '+ integration.name +' already exists'}
        return HttpResponse(content=json.dumps(errors), content_type="application/json", status=400)

    #Need to do this to honor the json response that is expected by the ajax client
    return HttpResponse(status=200, content=json.dumps({}), content_type="application/json")