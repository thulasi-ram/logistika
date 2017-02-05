$(document).ready(function() {

    $("myform").trigger("reset");

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
        data = response.data
        success = data.success
        msg = data.msg
        if (success == 'success'){
          Materialize.toast(msg ,5000,'green accent-4');
        }
        else{
          Materialize.toast(msg ,5000,'red accent-4');
        }
        });
        request.fail(function(jqXHR, textStatus) {
          Materialize.toast("Form submit failed. Please check network." ,5000,'red accent-4');
        });

        $('#submit_button').prop('disabled',false);


    });

});

});