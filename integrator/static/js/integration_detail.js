
function load_integration_detail(id){
    $.ajax({
        url:"integration/"+id,
        success:function(result){
            $("#main_container").html(result);
                $(".actions").click(function() {
                    window.location.hash = 'actions-' + $(this).attr('id').slice(8);
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

