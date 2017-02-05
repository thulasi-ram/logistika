$(document).ready(function() {
    $("myform").trigger("reset");
    $("#password").on("keyup",function(){
    if($(this).val())
        $("#remove_red_eye").show();
    else
        $("#remove_red_eye").hide();
    });
    $("#remove_red_eye").mousedown(function(){
                $("#password").attr('type','text');
            }).mouseup(function(){
            	$("#password").attr('type','password');
            }).mouseout(function(){
            	$("#password").attr('type','password');
            });
    $(function() {
    //hang on event of form with id=myform
    $("#myform").submit(function(e) {

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
                data: $("#myform").serialize(),
        });

        request.done(function(response) {
        });
        request.fail(function(jqXHR, textStatus) {
          Materialize.toast(jqXHR.responseText || "Form submit failed. Please check network." ,5000,'red accent-4');
        });

        $('#submit_button').prop('disabled',false);


    });

});

});