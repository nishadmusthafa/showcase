if (typeof String.prototype.startsWith != 'function') {
  String.prototype.startsWith = function (str){
    return this.slice(0, str.length) == str;
  };
};

load_by_hash();

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

window.onhashchange = function(event) {
    if (event.newURL == event.oldURL)
        return
    start_loading();
    load_by_hash();
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
    if (location.hash.startsWith('#actions'))
    {
        load_actions_page(location.hash);
        return;
    }

    if (location.hash.startsWith('#action_detail'))
    {
        load_action_detail_page(location.hash);
        return;
    }

    if (location.hash.startsWith('#add_action_form'))
    {
        id = location.hash.split('-')[1];
        addActionForm(id);
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
};

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
                    case 'success_int' :notificationType = "info"; 
                                        notificationMessage = "Integration created successfully"; 
                                        notifyTransaction(notificationType, notificationMessage);
                                        break;
                    }
            }

    }});
};

