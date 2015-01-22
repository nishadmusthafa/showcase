if (typeof String.prototype.startsWith != 'function') {
  String.prototype.startsWith = function (str){
    return this.slice(0, str.length) == str;
  };
}

load_by_hash();

var auth_fields;
var under_edit_auth_field = null;
var MANDATORY_AUTH_FIELD_FORM_FIELDS = ['element', 'source', 'display', 'field_type'];

function start_loading(){
    $("#main_container").html('<div class="row"> \
        <div class="col-md-offset-4"> \
            <h1>Loading... </h1> \
        </div> \
        </div>')
};

function coming_soon(){
    $("#main_container").html('<div class="row"> \
        <div class="col-md-offset-3"> \
            <h1>Coming soon..  to a monitor near you!!</h1> \
        </div> \
        </div>')
};


function load_by_hash(){
    if (location.hash.length == 0)
    {
        load_index_page();
        return
    }

    if (location.hash.startsWith('#index'))
    {
        load_index_page(location.hash);
        return
    }
    if (location.hash == '#create_integration')
    {
        load_integration_form();
        return;
        }
    if (location.hash.startsWith('#integration_detail'))
    {
        id = location.hash.split('-')[1];
        load_integration_detail(id);
        return;
    }
    if (location.hash.startsWith('#add_action'))
    {
        id = location.hash.split('-')[1];
        add_action(id);
        return;
    }
    if (location.hash.startsWith('#agent_sync'))
    {
        id = location.hash.split('-')[1];
        agent_sync(id);
        return;
    }
    if (location.hash.startsWith('#auth_validation'))
    {
        id = location.hash.split('-')[1];
        auth_validation(id);
        return;
    }
    if (location.hash.startsWith('#contact_sync'))
    {
        id = location.hash.split('-')[1];
        contact_sync(id);
        return;
    }
    if (location.hash.startsWith('#interaction_retrieval'))
    {
        id = location.hash.split('-')[1];
        interaction_retrieval(id);
        return;
    }
}

function load_index_page(hash){
    $.ajax({
        url:"integration/",
        success:function(result){
            $("#main_container").html(result);
            $("#add_integration").click(create_integration_form);
            $(".integration_detail").click(function() {
                window.location.hash = '#integration_detail-' + $(this).attr('id');
            });
            if (hash != undefined && hash.split("-").length > 1) {
                switch(hash.split("-")[1])
                {
                    case 'success_int' :notification_type = "info"; 
                                        notification_message = "Integration created successfully"; 
                                        notify_transaction(notification_type, notification_message);
                                        break;
                    }
            }

    }});
};

function add_action(id){
    coming_soon();
};

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

function load_integration_detail(id){
    $.ajax({
        url:"integration/"+id,
        success:function(result){
            $("#main_container").html(result);
                $(".add_action").click(function() {
                    window.location.hash = '#add_action-' + $(this).attr('id');
                });
                $(".agent_sync").click(function() {
                    window.location.hash = '#agent_sync-' + $(this).attr('id');
                });
                $(".auth_validation").click(function() {
                    window.location.hash = '#auth_validation-' + $(this).attr('id');
                });
                $(".contact_sync").click(function() {
                    window.location.hash = '#contact_sync-' + $(this).attr('id');
                });
                $(".interaction_retrieval").click(function() {
                    window.location.hash = '#interaction_retrieval-' + $(this).attr('id');
                });
            
     }});
};

function notify_transaction(message_type, message){
    $("#notification_window").
    html('<div class="alert alert-'+ message_type +' alert-dismissible fade in" role="alert">\
        <button type="button" class="close" data-dismiss="alert" aria-label="Close">\
        <span aria-hidden="true">×</span>\
        </button>'+ message +'</div>');
}

window.onhashchange = function(event) {
    if (event.newURL == event.oldURL)
        return
    start_loading();
    load_by_hash();
};

function load_integration_form()
{
    auth_fields = {};
    $.ajax({
        url:"integration_create/form/",
        success:function(result){
            $("#main_container").html(result);
            $("#add_auth_field").click(add_auth_field_form);
            $("#auth_field_form_submit").click(save_auth_field);
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
                    'auth_field_list': auth_fields,
                    'auth_validation_endpoint': $("#auth_validation_endpoint").val(),
                    'contact_synchronization_endpoint': $("#auth_validation_endpoint").val(),
                    'interaction_retrieval_endpoint': $("#auth_validation_endpoint").val(),
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
              for (key in result.responseJSON)
              {
                flag_form_field(key, result.responseJSON[key]);
              }
            }
          },
    });
};

function add_auth_field_form(){
    clear_auth_field_form();
    $("#auth_field_modal").modal('show');
};

function get_auth_field_data(){
    var auth_field_data = {};
    auth_field_data["element"] = $("#element").val();
    auth_field_data["source"] = $("#source").val();
    auth_field_data["display"] = $("#display").val();
    auth_field_data["help_text"] = $("#help_text").val();
    auth_field_data["field_format"] = $("#field_format").val();
    auth_field_data["field_type"] = $("#field_type").val();
    auth_field_data["mandatory"] = $("#mandatory").is(":checked");
    auth_field_data["store"] = $("#store").is(":checked");
    return auth_field_data;
};

function set_auth_field_data(auth_field_data){
    $("#element").val(auth_field_data["element"]);
    $("#source").val(auth_field_data["source"]);
    $("#display").val(auth_field_data["display"]);
    $("#help_text").val(auth_field_data["help_text"]);
    $("#field_format").val(auth_field_data["field_format"]);
    $("#field_type").val(auth_field_data["field_type"]);
    $("#mandatory").prop('checked', auth_field_data["mandatory"]);
    $("#store").prop('checked', auth_field_data["store"]);
};

function refresh_auth_field_list(){
    $("#auth_field_list").html('');
    var keys = Object.keys(auth_fields);
    keys.sort();
    len = keys.length;
    for (i = 0; i < len; i++)
    {
        k = keys[i];
        $("#auth_field_list").append('<li id=\"list_'+ auth_fields[k]["element"] +'\">'+ auth_fields[k]["display"] +' - <a style="cursor: pointer;" class=\"edit_auth_field\">Edit</a>/<a style="cursor: pointer;" class=\"delete_auth_field\">Delete</a></li>');
    }
    $(".edit_auth_field").click(function() {
            edit_auth_field($(this).parent().attr('id'));
        });
    $(".delete_auth_field").click(function() {
            delete_auth_field($(this).parent().attr('id'));
        });
};

function edit_auth_field(specific_id){
    clear_auth_field_form();
    var key = specific_id.replace("list_", "");
    set_auth_field_data(auth_fields[key]);
    under_edit_auth_field = key;
    $("#auth_field_modal").modal('show');
};

function delete_auth_field(specific_id){
    var key = specific_id.replace("list_", "");
    delete auth_fields[key];
    refresh_auth_field_list();
};

function clear_auth_field_form()
{
    var auth_field_data = {};
    auth_field_data["element"] = "";
    auth_field_data["source"] = "input";
    auth_field_data["display"] = "";
    auth_field_data["help_text"] = "";
    auth_field_data["field_format"] = "";
    auth_field_data["field_type"] = "input";
    auth_field_data["mandatory"] = false;
    auth_field_data["store"] = false;
    set_auth_field_data(auth_field_data);
    $("#auth_field_modal .form-group").removeClass('has-error');
    $("#auth_field_modal .help-block").hide();

};

function flag_form_field(field_name, reason){
    var element = $("#" + field_name);
    while (!element.hasClass('form-group'))
    {
        element = element.parent()
    }
    element.addClass('has-error');
    element.find('.help-block').html(reason);
    element.find('.help-block').show()
};

function validate_auth_field_input(auth_field_data){
    var valid = true;
    for(var i = 0; i < MANDATORY_AUTH_FIELD_FORM_FIELDS.length; i++)
    {
        if (auth_field_data[MANDATORY_AUTH_FIELD_FORM_FIELDS[i]] == ""){
            flag_form_field(MANDATORY_AUTH_FIELD_FORM_FIELDS[i], 
                            MANDATORY_AUTH_FIELD_FORM_FIELDS[i] + " is mandatory");
            valid = false;
        }
    }
    
    if (under_edit_auth_field == null && auth_field_data['element'] in auth_fields){
        flag_form_field("element", 
                        "Auth Field with element name "+ auth_field_data['element'] +" already exists"); 
        valid = false;
    }
    return valid;
};

function save_auth_field(){
    var auth_field_data = get_auth_field_data();
    if(!validate_auth_field_input(auth_field_data))
    return
    
    auth_fields[auth_field_data['element']] = auth_field_data;
    if (under_edit_auth_field != null){
        // Special case when the element name(unique key) 
        // is being changed in an edit
        if (under_edit_auth_field != auth_field_data['element'])
        delete auth_fields[under_edit_auth_field];

        under_edit_auth_field = null
    }

    refresh_auth_field_list();
    clear_auth_field_form();
    $("#auth_field_modal").modal('hide');
};

