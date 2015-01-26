var inputParamsModalInput;
var httpRequestParamsModalInput;
function addActionForm(id){
    input_params = {}
    $.ajax({
        url:"integration/"+id+"/add/action/form/",
        success:function(result){
            $("#main_container").html(result);
            inputParamsModalInput = $("#action_input_params").modalInputField({
                "mandatory": ['key', 'name'],
                "unique": "key",
                "label": "Input Params (Talkdesk to Bridge)",
                "text": "Add Input Param",
                "modal": "input_param_modal",
                "modalForm": "input_param_form",
            });
            $("#api_type").change(function (event){
                changeApiType($(this).find("option:selected").val());
            });
            $(".help-block").hide();
            $("#rest_api").hide();
            $("#soap_api").hide();
            $("#oauth_workflow").hide();
            $('#add_action').click(function(e) {
                    e.preventDefault();   
                    addAction(id);
                });
        }});
};


function addAction(id){
    action_data = {
                    'name': $("#name").val(),
                    'display': $("#display").val(),
                    'description': $("#description").val(),
                    'input_param_list': inputParamsModalInput.getFields(),
                    'external_request': buildExternalRequest()
                }
    $.ajax({
        url:"integration/"+ id +"/action/add/",
        success:function(){
            window.location.hash = "actions-"+id+"-success_action";
        },
        headers: { "X-CSRFToken": $.cookie('csrftoken')},
        type: 'POST',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(action_data),
        dataType: 'json',
        statusCode: {
            400: function(result) {
              $(".help-block").hide();
              $(".form-group").removeClass('has-error');
              for (key in result.responseJSON)
              {
                flagFormField(key, result.responseJSON[key]);
              }
            }
          },
    });
};

function buildExternalRequest(){
    var data = {};
    switch($("#api_type").val()){
        case 'rest': data = buildRestRequest();
                     break;
        case 'soap': data = buildSoapRequest();
                     break;
        case 'oauth': data = buildOAuthRequest();
                     break;
        default: data = {};
    }
    return data;
};

function buildRestRequest()
{
    data = {};
    data['type'] = "rest";
    data['request_params'] = $("#http_request_params").val();
    data['http_url'] = $("#http_url").val();
    data['http_method'] = $("#http_method").val();
    data['basic_auth'] = $("#basic_auth").val();
    data['success_response'] = $("#success_response").val();
    return data;
};

function buildSoapRequest(){
    //TODO
    return {};
};

function buildOAuthRequest(){
    //TODO
    return {};
};

function changeApiType(type){
    if (type == "rest"){
        $("#rest_api").show();
        $("#soap_api").hide();
        $("#oauth_workflow").hide();
    }
    else if (type == "soap")
    {
        $("#oauth_workflow").hide();
        $("#soap_api").show();
        $("#rest_api").hide();
    }
    else if (type == "oauth")
    {
        $("#oauth_workflow").show();
        $("#soap_api").hide();
        $("#rest_api").hide();
    }

    else if (type == "none")
    {
        $("#soap_api").hide();
        $("#rest_api").hide();
        $("#oauth_workflow").hide();
    }
}

function agent_sync(id){
    coming_soon();
};

function auth_validation(id){
    coming_soon();
};

function contact_sync(id){
    coming_soon();
};

function interaction_retrieval(id){
    coming_soon();
};
