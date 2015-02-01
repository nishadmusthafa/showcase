from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from integrator.helper import serialize_action, serialize_integration
from integrator.models import Action, Integration
import json
import logging

logger = logging.getLogger('django')

def get_integration_json(request, integration_id):
    logger.info('Input integration_id : %s' % (integration_id))
    try:
        integration = Integration.objects.get(name=integration_id)
    except Integration.DoesNotExist:
        logger.error('%s does not exist' % (integration_id))
        return HttpResponseNotFound('<h1>Page not found</h1>')

    integration = serialize_integration(request, integration)
    logger.info("serialized output: %s" % integration)
    return HttpResponse(status=200, content=json.dumps(integration), content_type="application/json")

def get_action_json(request, integration_id, action_id):
    logger.info('Input integration_id : %s action_id : %s' % (integration_id, action_id))
    try:
        action = Action.objects.get(provider=integration_id, name=action_id)
    except Action.DoesNotExist:
        logger.error('%s,%s does not exist' % (integration_id, action_id))
        return HttpResponseNotFound('<h1>Page not found</h1>')

    action = serialize_action(request, action)
    logger.info("serialized output: %s" % action)
    return HttpResponse(status=200, content=json.dumps(action), content_type="application/json")
