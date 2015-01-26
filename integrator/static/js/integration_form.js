var authFieldModalInput;

function load_integration_form()
{
    auth_fields = {};
    $.ajax({
        url:"integration_create/form/",
        success:function(result){
            $("#main_container").html(result);
            authFieldModalInput = $("#auth_field_list").modalInputField({
                "mandatory": ['element', 'source', 'display', 'field_type'],
                "unique": "element",
                "label": "Auth Fields",
                "text": "Add Auth Field",
                "modal": "auth_field_modal",
                "modalForm": "auth_field_form",
            });
            $(".help-block").hide();
            $('#create_integration_form').submit(function(e) {
                    e.preventDefault();   
                    create_integration();
                });
    }});
}

function create_integration_form(){
    window.location.hash = "create_integration";
};


function create_integration(){
    integration_data = {
                    'name': $("#name").val(),
                    'display_name': $("#display_name").val(),
                    'description': $("#description").val(),
                    'logo_url': $("#logo_url").val(),
                    'icon_url': $("#icon_url").val(),
                    'authentication_type': $("#authentication_type").val(),
                    'auth_field_list': authFieldModalInput.getFields(),
                }
    $.ajax({
        url:"integration_create/",
        success:function(){
            window.location.hash = "index-success_int";
        },
        headers: { "X-CSRFToken": $.cookie('csrftoken')},
        type: 'POST',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(integration_data),
        dataType: 'json',
        statusCode: {
            400: function(result) {
              $(".form-group").removeClass('has-error');
              $(".help-block").hide();
              for (key in result.responseJSON)
              {
                flagFormField(key, result.responseJSON[key]);
              }
            }
          },
    });
};