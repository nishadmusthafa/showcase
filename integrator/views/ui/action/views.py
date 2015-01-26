from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
import json
from integrator.models import Action, ActionInputParam, Integration
from integrator.validate import validate_action_form_data
from mongoengine.errors import NotUniqueError

def get_integration_actions(request, integration_id):
    try:
        integration = Integration.objects.get(name=integration_id)
    except Integration.DoesNotExist:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    actions = Action.objects.filter(provider=integration_id)
    context = {
                'actions': actions,
                }
    return render(request, 'actions.html', context)

def add_action_form(request, integration_id):
    try:
        integration = Integration.objects.get(name=integration_id)
    except Integration.DoesNotExist:
        return HttpResponseNotFound('<h1>Page not found</h1>')

    context = {'auth_fields': integration.authentication_configuration}
    return render(request, 'add_action.html', context)

def action_detail(request, integration_id, action_id):
    try:
        action = Action.objects.get(provider=integration_id, name=action_id)
    except Action.DoesNotExist:
        return HttpResponseNotFound('<h1>Page not found</h1>')

    context = {'action': action}
    return render(request, 'action_detail.html', context)

def add_action(request, integration_id):
    if not request.is_ajax():
        return HttpResponse(status=400)

    try:
        integration = Integration.objects.get(name=integration_id)
    except Integration.DoesNotExist:
        return HttpResponseNotFound('<h1>Page not found</h1>')

    action_data = {}
    for key, value in json.loads(request.body).iteritems():
        if value:
            action_data[key] = value

    is_valid, errors = validate_action_form_data(action_data)

    
    if not is_valid:
        return HttpResponse(content=json.dumps(errors), content_type="application/json", status=400)
    
    input_param_list = action_data.get('input_param_list', {})
    if input_param_list:
        del(action_data['input_param_list'])

    action = Action(**action_data)
    for key, value in input_param_list.iteritems():
        data = {'key': key}
        data.update(value)
        embedded_input_params = ActionInputParam(**data)
        action.inputs.append(embedded_input_params)

    action.provider = integration_id

    try:
        action.save(force_insert=True)
    except NotUniqueError:
        errors = {'name': 'Action with name '+ action.name +' already exists'}
        return HttpResponse(content=json.dumps(errors), content_type="application/json", status=400)

    return HttpResponse(status=200, content=json.dumps({}), content_type="application/json")