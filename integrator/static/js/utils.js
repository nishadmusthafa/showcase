if (typeof String.prototype.startsWith != 'function') {
  String.prototype.startsWith = function (str){
    return this.slice(0, str.length) == str;
  };
};

function formatVarString(templateString, fillers)
{

    var pattern = new RegExp('{([1-' + fillers.length + '])}','g');
    var formattedString = String(templateString).replace(pattern, function(match, index) { return fillers[index - 1]; });
    return formattedString;
}

function flagFormField(field_name, reason){
    var element = $("#" + field_name);
    while (!element.hasClass('form-group'))
    {
        element = element.parent()
    }
    element.addClass('has-error');
    element.find('.help-block').html(reason);
    element.find('.help-block').show()
};


function notifyTransaction(messageType, message){
    $("#notification_window").
    html('<div class="alert alert-'+ messageType +' alert-dismissible fade in" role="alert">\
        <button type="button" class="close" data-dismiss="alert" aria-label="Close">\
        <span aria-hidden="true">×</span>\
        </button>'+ message +'</div>');
};

function resetForm(form) {
    form.find('input:text, input:password, input:file, textarea').val('');
    form.find('option[class=default]').attr('selected', 'selected');
    form.find(".form-group").removeClass('has-error');
    form.find(".help-block").hide();
    form.find('input:radio, input:checkbox')
         .removeAttr('checked').removeAttr('selected');
}

(function ( $ ) {
    $.fn.modalInputField = function(params) {
        var vars = $(this).data('modalInputField');
        if (!vars) {
            vars = {
                    template: '<label class="col-sm-2 control-label">{1}</label>\
                                <div class="col-sm-4">\
                                <button class="btn btn-primary btn-sm add_modal_field" type="button">{2}</button>\
                                <div class="row">\
                                <ul style="list-style: none;" class="field_list"></ul>\
                                </div>\
                                <span class="help-block" ></span>\
                                </div>',
                    fields: {},
                    underEdit : null,
                    mandatory : params["mandatory"],
                    modal : $("#"+params["modal"]),
                    modalForm : $("#"+params["modalForm"]),
                    unique : params["unique"],
                    modalInput: $(this),
                    label: params["label"],
                    text: params["text"],
                };
            $(this).data('modalInputField', vars);   
        };
        vars.modalInput.html(formatVarString(vars.template, [vars.label, vars.text]));
        vars.modalInput.find('.add_modal_field').click(function(){
            bringUpModal(vars);
        });
        vars.modal.find('.submit-modal-input').click(function(){
            addField(vars);
        });
        return this;
    };

    $.fn.getFields = function(){
        var vars = $(this).data('modalInputField');
        return vars.fields;
    };

    $.fn.fieldUpdate = function(listener){
        var vars = $(this).data('modalInputField');
        vars["changeListener"] = listener;
    };

    function bringUpModal(vars)
    {   
        resetForm(vars.modalForm);
        vars.modal.modal('show');
    }

    function getFieldData(vars)
    {
        var fieldData = {};
        vars.modalForm.find('input, select, textarea').each(function(){
            if ($(this).attr('type') == "checkbox")
                fieldData[$(this).attr('id')] = $(this).is(":checked");
            else 
                fieldData[$(this).attr('id')] = $(this).val();
        });
        return fieldData;
    };

    function setFieldData(vars, fieldData){
        vars.modalForm.find('input, select, textarea').each(function(){
            if($(this).attr('type') == "checkbox")
                $(this).prop('checked', fieldData[$(this).attr('id')]);
            else 
                $(this).val(fieldData[$(this).attr('id')]);
        });
    };

    function validateInput(vars, fieldData){
        var valid = true;
        for(var i = 0; i < vars.mandatory.length; i++)
        {
            if (fieldData[vars.mandatory[i]] == ""){
                flagFormField(vars.mandatory[i], vars.mandatory[i] + " is mandatory");
                valid = false;
            }
        }
        
        if (vars.underEdit == null && fieldData[vars.unique] in vars.fields){
            flagFormField(vars.unique, 
                          vars.unique + " name "+ fieldData[vars.unique] +" already exists"); 
            valid = false;
        }
        return valid;
    };

    function addField(vars){
        var fieldData = getFieldData(vars);
        
        if(!validateInput(vars, fieldData))
        return;
        
        vars.fields[fieldData[vars.unique]] = fieldData;
        if (vars.underEdit != null){
            // Special case when the element name(unique key) 
            // is being changed in an edit
            if (vars.underEdit != fieldData[vars.unique])
            delete vars.fields[vars.underEdit];

            vars.underEdit = null
        }

        refreshFieldList(vars);
        resetForm(vars.modalForm);
        vars.modal.modal('hide');
    };

    function editField(vars, id){
        resetForm(vars.modalForm);
        var key = id.replace("list_", "");
        setFieldData(vars, vars.fields[key])
        vars.underEdit = key;
        vars.modal.modal('show');
    };

    function deleteField(vars, id){
        var key = id.replace("list_", "");
        delete vars.fields[key];
        refreshFieldList(vars);
    };

    function refreshFieldList(vars){
        vars.modalInput.find(".field_list").html('');
        var keys = Object.keys(vars.fields);
        keys.sort();
        len = keys.length;
        for (i = 0; i < len; i++)
        {
            k = keys[i];
            vars.modalInput.find(".field_list").append('<li id=\"list_'+ vars.fields[k][vars.unique] +'\">'+ vars.fields[k][vars.unique] +' - <a style="cursor: pointer;" class=\"edit_field\">Edit</a>/<a style="cursor: pointer;" class=\"delete_field\">Delete</a></li>');
        }
        vars.modalInput.find(".edit_field").click(function() {
                editField(vars, $(this).parent().attr('id'));
            });
        vars.modalInput.find(".delete_field").click(function() {
                deleteField(vars, $(this).parent().attr('id'));
            });
        if (vars.changeListener)
            vars.changeListener();
    };
 
}( jQuery ));