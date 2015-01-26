function load_actions_page(hash){
    integration_id = hash.split('-')[1]
    $.ajax({
        url:"/integration/"+ integration_id +"/action/",
        success:function(result){
            $("#main_container").html(result);
            $("#add_action").click(function (){
                add_action_form(integration_id);
            });
            $(".action_detail").click(function() {
                window.location.hash = '#action_detail-' + integration_id + '-' + $(this).attr('id');
            });
            if (hash != undefined && hash.split("-").length > 2) {
                switch(hash.split("-")[2])
                {
                    case 'success_action' :notificationType = "info"; 
                                        notificationMessage = "Action added successfully"; 
                                        notifyTransaction(notificationType, notificationMessage);
                                        break;
                    }
            }

    }});
};

function add_action_form(integration_id){
    window.location.hash = 'add_action_form-' + integration_id;
};
