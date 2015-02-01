def serialize_integration(request, integration):
    auth_conf_list = []
    for auth_conf in integration.authentication_configuration:
        auth_conf_item = {}
        auth_conf_item['source'] = auth_conf.source
        auth_conf_item['display'] = auth_conf.display
        auth_conf_item['type'] = auth_conf.field_type
        auth_conf_item['format'] = auth_conf.field_format
        auth_conf_item['help'] = auth_conf.help_text
        auth_conf_item['store'] = auth_conf.store
        auth_conf_item['mandatory'] = auth_conf.mandatory
        auth_conf_list.append({
                                auth_conf.element: auth_conf_item
                              })

    serialized_integration = {}
    serialized_integration['name'] = integration.name
    serialized_integration['display_name'] = integration.display_name
    serialized_integration['description'] = integration.description
    serialized_integration['logo_url'] = integration.logo_url
    serialized_integration['icon_url'] = integration.icon_url
    serialized_integration['authentication_type'] = integration.authentication_type
    serialized_integration['authentication_configuration'] = auth_conf_list
    serialized_integration['auth_validation_endpoint'] = request.build_absolute_uri('/integrations/') + integration.name + "/auth_validation/"
    serialized_integration['contact_synchronization_endpoint'] = request.build_absolute_uri('/integrations/') + integration.name + "/contact_sync/"
    serialized_integration['interaction_retrieval_endpoint'] = request.build_absolute_uri('/integrations/') + integration.name + "/interaction_retrieval/"
    serialized_integration['agent_synchronization_endpoint'] = request.build_absolute_uri('/integrations/') + integration.name + "/agent_sync/"
    serialized_integration['interaction_types'] = integration.interaction_types

    return serialized_integration

def serialize_action(request, action):
    input_param_list = []
    for action_input_param in action.inputs:
        input_param = {}
        input_param['key'] = action_input_param.key
        input_param['name'] = action_input_param.name
        input_param['mandatory'] = action_input_param.mandatory
        input_param_list.append(input_param)

    serialized_action = {}
    serialized_action['provider'] = action.provider
    serialized_action['name'] = action.name
    serialized_action['display'] = action.display
    serialized_action['description'] = action.description
    serialized_action['endpoint'] = request.build_absolute_uri('/integrations/') + action.provider + "/actions/" + action.name + "/"
    serialized_action['inputs'] = input_param_list
    return serialized_action




