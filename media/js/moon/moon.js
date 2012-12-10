//JQuery csrf_setup
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function sameOrigin(url) {
    var host = document.location.host;
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        !(/^(\/\/|http:|https:).*/.test(url));
}

var csrftoken = getCookie('csrftoken');
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

var resizeSelectWidth = function ($form) {
    var maxWidth = 0, newMaxWidth = 0, i,
        $selects = $form.find('tr.FormData > td.DataTD > select.FormElement'),
        cn = $selects.length;

    // calculate the max width of selects
    for (i = 0; i < cn; i += 1) {
        maxWidth = Math.max(maxWidth, $($selects[i]).width());
    }
    maxWidth += 2; // increase width to improve visibility

    // change the width of selects to the max width
    for (i = 0; i < cn; i += 1) {
        $($selects[i]).width(maxWidth);
        newMaxWidth = Math.max(maxWidth, $($selects[i]).width());
    }
};

function loadAndParseIntoMain(url) {
    dojo.xhrGet({
        url: url,
        load: function(data){
            if (dojo.byId("onAjaxLoad")) {
                dojo.forEach(dijit.findWidgets(dojo.byId("onAjaxLoad")), function(w) {
                    w.destroyRecursive();
                });
                dojo.destroy("onAjaxLoad");
            }
            dojo.byId("content_view").innerHTML = data;
            dojo.parser.parse(dojo.byId("onAjaxLoad"));
        }
    });
}

function loadAndRunIntoMain(url) {
    dojo.xhrGet({
        url: url,
        load: function(data){
            dojo.byId("content_view").innerHTML = data;
            eval(dojo.byId("onAjaxLoad").innerHTML);
        }
    });
}

function checkFormError(response, postdata) {
    var success = response.success;
    var error_msg = '';
    var error = $.parseJSON(response.responseText);

    if (error.server_error) {
        error_msg = error.server_error;
        success = false;
    }

    return [success,error_msg,1];
}

function ErrorDialog(message){
    var ok_cancel_dialog = $('<div></div>')
        .html(message)
        .dialog({
            title: "Ошибка!",
            height: 160,
            modal: true,
            buttons: {
                'Отмена': function () {
                    $(this).remove();
                }
            }
        });
}
function DoAction(action_url,action,id) {
    console.log(action_url,action,id);
    $.getJSON( action_url,
        {
            action: action,
            id: id
        }
        , function(data){
            if (!data.success) {
                ErrorDialog(data.error);
            } else {
                $("#mygrid").trigger( 'reloadGrid' );
            }

        });
}

function DoActionVsDialog(action_url,message,title,action,id) {
    console.log(action_url,message,title,action,id);
    var ok_cancel_dialog = $('<div></div>')
        .html(message)
        .dialog({
            title: title,
            resizable: false,
            height: 160,
            modal: true,
            buttons: {
                'Отмена': function () {
                    $(this).remove();
                },
                'Продолжить' : function () {

                    DoAction(action_url,action,id);
                    $(this).remove();
                }
            }
        });
}

function DoActionVsDialogForm(action_url,form_url,title,action,id) {
    $.get( form_url, {action:action,id:id},
        function (data, textStatus, XMLHttpRequest){
            var ok_cancel_dialog = $('<div></div>')
                .html(data)
                .dialog({
                    title: title,
                    resizable: false,
                    modal: true,
                    beforeClose: function (){
                        $(this).remove();
                    },
                    buttons: {
                        'Отмена': function () {
                            $(this).remove();
                        },
                        'Продолжить' : function () {
                            var request = {action:action,id:id};
                            var ok = true;
                            $(".FormElement")
                                .each(function(index,elem){
                                    console.log(index,elem,$(elem).val());
                                    request[$(elem).attr('id')] = $(elem).val();
                                    if (request[$(elem).attr('id')] == '' && $(elem).hasClass('FormRequired') ) {
                                        ok = false}
                                });

                            if (ok == true){
                                $.getJSON( action_url,
                                    request,
                                    function(data){
                                        if (!data.success) {
                                            ErrorDialog(data.error);
                                        } else {
                                            $("#mygrid").trigger( 'reloadGrid' );
                                        }

                                    });
                                $(this).remove();
                            }
                        }
                    }
                });
    }

    );

}
