$(document).ready(function() {
    $(".dropdown-button").dropdown();
    $('.modal').modal();

    $("#signup_password").on("keyup",function(){
    if($(this).val())
        $("#remove_red_eye").show();
    else
        $("#remove_red_eye").hide();
    });
    $("#remove_red_eye").mousedown(function(){
                $("#signup_password").attr('type','text');
            }).mouseup(function(){
            	$("#signup_password").attr('type','password');
            }).mouseout(function(){
            	$("#signup_password").attr('type','password');
            });

    $(function() {
    //hang on event of form with id=myform
    $("#login").submit(function(e) {

        //prevent Default functionality
        e.preventDefault();
         $('#submit_button').prop('disabled',true);
        //get the action-url of the form
        var actionurl = e.currentTarget.action;
        //do your own request an handle the results
        var request = $.ajax({
                url: actionurl,
                type: 'post',
                dataType: 'json',
                data: $("#login").serialize(),
        });

        request.done(function(response) {
            window.location.replace(response.redirect);
        });
        request.fail(function(jqXHR, textStatus) {
          Materialize.toast(jqXHR.responseText || "Form submit failed. Please check network." ,5000,'red accent-4');
        });
        $('#submit_button').prop('disabled',false);
    });
    });

    $(function() {
    //hang on event of form with id=myform
    $("#signup").submit(function(e) {

        //prevent Default functionality
        e.preventDefault();
         $('#submit_button').prop('disabled',true);
        //get the action-url of the form
        var actionurl = e.currentTarget.action;
        //do your own request an handle the results
        var request = $.ajax({
                url: actionurl,
                type: 'post',
                dataType: 'json',
                data: $("#login").serialize(),
        });

        request.done(function(response) {
            window.location.replace(response.redirect);
        });
        request.fail(function(jqXHR, textStatus) {
          Materialize.toast(jqXHR.responseText || "Form submit failed. Please check network." ,5000,'red accent-4');
        });
        $('#submit_button').prop('disabled',false);
    });

});
});