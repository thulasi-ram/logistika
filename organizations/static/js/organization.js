$(document).ready(function() {
    get_org_list();

    $("#onboard_req_form").submit(function(e) {
        e.preventDefault();
         $('#onboard_req_submit').prop('disabled',true);
        var action_url = e.currentTarget.action;
        var request = $.ajax({
                url: action_url,
                type: 'post',
                dataType: 'json',
                data: $("#onboard_req_form").serialize(),
        });
        request.done(function(response) {
            Materialize.toast(response,5000,'green accent-4');
            $("#onboard_req_form").trigger("reset");
        });
        request.fail(function(jqXHR, textStatus) {
          Materialize.toast(jqXHR.responseText || "Form submit failed. Please check network." ,5000,'red accent-4');
        });
        $('#onboard_req_submit').prop('disabled',false);
    });

});

function get_org_list() {
    var request = $.ajax({
        'url': '/organizations/list',
        contentType: 'application/json'
    });
    request.done(function(response) {
        $('input.autocomplete').autocomplete({ data: response, limit: 20,});
    });
    request.fail(function(jqXHR, textStatus) {
    });
};