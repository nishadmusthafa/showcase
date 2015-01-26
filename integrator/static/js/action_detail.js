function load_action_detail_page(hash){
    integration_id = hash.split('-')[1]
    action_id = hash.split('-')[2]
    $.ajax({
        url:"integration/"+integration_id+"/action/"+action_id+"/",
        success:function(result){
            $("#main_container").html(result);
     }});
};

