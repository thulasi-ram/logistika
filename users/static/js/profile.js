$(document).ready(function() {
    $('ul.tabs').tabs('select_tab', 'account');
    if ($(".dropdown-button").length){
    $('#profile_image_display').onclick = function() {
    $('#profile_image').click();
       };}
    $("#password_change").submit(function(e) {

        //prevent Default functionality
        e.preventDefault();
         $('#password_reset_submit').prop('disabled',true);
        //get the action-url of the form
        var actionurl = e.currentTarget.action;
        //do your own request an handle the results
        var request = $.ajax({
                url: actionurl,
                type: 'post',
                dataType: 'json',
                data: $("#password_change").serialize(),
        });

        request.done(function(response) {
            Materialize.toast(response.responseText,5000,'green accent-4');
            $("#password_change").find("input[type=password], textarea").val("");
        });
        request.fail(function(jqXHR, textStatus) {
          Materialize.toast(jqXHR.responseText || "Form submit failed. Please check network." ,5000,'red accent-4');
        });
        $('#password_reset_submit').prop('disabled',false);
    });
});