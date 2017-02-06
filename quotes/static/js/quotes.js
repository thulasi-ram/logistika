$(document).ready(function() {
var hash = window.location.hash.substr(1);
default_tab = 'list_quotes'
if( hash == 'create'){
default_tab = 'create_quotes'
}
else if(hash == 'compare'){
default_tab = 'compare_quotes'
}
$('ul.tabs').tabs('select_tab', default_tab);

get_quotes_list();

    $("#create_quotes_form").submit(function(e) {

        //prevent Default functionality
        e.preventDefault();
         $('#create_quote_submit').prop('disabled',true);
        //get the action-url of the form
        var actionurl = e.currentTarget.action;
        //do your own request an handle the results
        var request = $.ajax({
                url: actionurl,
                type: 'post',
                dataType: 'json',
                data: $("#create_quotes_form").serialize(),
        });

        request.done(function(response) {
            Materialize.toast(response ,5000,'green accent-4');
            $("#create_quotes_form").find("input[type=text], textarea").val("");
            get_quotes_list();
        });
        request.fail(function(jqXHR, textStatus) {
          Materialize.toast(jqXHR.responseText || "Form submit failed. Please check network." ,5000,'red accent-4');
        });

        $('#create_quote_submit').prop('disabled',false);


    });

});

function get_quotes_list() {
    var request = $.ajax({
        'url': '/quotes/listing',
        contentType: 'application/json'
    });
    request.done(function(response) {
        Materialize.toast(response.data ,5000,'green accent-4');
    });
    request.fail(function(jqXHR, textStatus) {
        Materialize.toast(jqXHR.responseText || "Form submit failed. Please check network." ,5000,'red accent-4');
    });
};