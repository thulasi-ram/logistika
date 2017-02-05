$(document).ready(function() {

//    reset();
    get_user_list();
    $('#treebo_poc').change(set_user_id);

    $(function() {
    //hang on event of form with id=myform
    $("#myform").submit(function(e) {

        //prevent Default functionality
        e.preventDefault();
         $('#corporate_submit_button').prop('disabled',true);
         $('#corporate_submit_button').css("background-color","yellow");
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
        redirect_url = data.redirect_url
        if (success == 'success'){
          Materialize.toast(msg ,5000,'green accent-4');
          setTimeout(function () {
              window.location.href = redirect_url;
            }, 2500);

        }
        else{
          Materialize.toast(msg ,5000,'red accent-4');
          $('#corporate_submit_button').prop('disabled',false);
          $('#corporate_submit_button').css("background-color","#11d05d");
        }
        });
        request.fail(function(jqXHR, textStatus) {
          Materialize.toast("Error occured. Please try again after some time." ,5000,'red accent-4');
          $('#corporate_submit_button').prop('disabled',false);
          $('#corporate_submit_button').css("background-color","#11d05d");
        });


    });

});

});

function get_user_list() {
    var request = $.ajax({
        'url': '/corporate_bookings/get_user_list',
        contentType: 'application/json'
    });
    request.done(function(response) {
        userList = response.data.users
        val = 1
        for (var i = 0; i < userList.length; i++) {
            val++
            var user = new Option(userList[i]['name'], userList[i]['id']);
            $("#treebo_poc").append(user);
        }
    });
    request.fail(function(jqXHR, textStatus) {
    });
};

function set_user_id(){
    userId = $(this).val();
   $("#user_id").val(userId);

};

function reset(){
    $('input[type=text]').val('');
    $('input[type=number]').val('');
    $('input[type=select]').val('');
    $('input[type=radio]').val('');
    $('input[type=checkbox]').val('');
}