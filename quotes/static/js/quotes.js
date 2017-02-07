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
get_quotes_list(1);

    $("#list_quotes_pagination").on("click", "li", function(event){
    var value = this.textContent;
    get_quotes_list.call(this, value)
//    $.when(get_quotes_list(value)).done(function(){
//    $('#list_quotes_pagination li').removeClass('active');
//    $(this).addClass('active');
//    });

});


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

function get_quotes_list(page) {
    var url = '/quotes/listing/?page='+page
    var request = $.ajax({
        'url': url,
        contentType: 'application/json'
    });
    var self = this;
    request.done(function(response) {
        $quote_listing = $("#list_quotes").find('tbody')
        $quote_listing.empty()
        if (response.quotes){
        curr_page = parseInt(response.curr_page) || 1
        total_pages = parseInt(response.total_pages) || 1
        items_per_page = parseInt(response.items_per_page) || 10
        quotes = JSON.parse(response.quotes);
        for (var  i = 0 ; i < quotes.length ; i++) {
            $quote_listing.append('<tr><td>'+(items_per_page*(curr_page - 1)+i + 1)+'</td><td>'+quotes[i].title+'</td><td>$0.87</td></tr>')
        }}
        $paginator =  $("#list_quotes_pagination li:last");
        $("#list_quotes_pagination li.page_numbers").remove();
        for (var j = 0; j< total_pages; j++){
            $paginator.before('<li class="waves-effect page_numbers"><a href="#">'+(j+1)+'</a></li>');
            $('#list_quotes_pagination li:nth-child(2)').addClass('active');
        }
        Materialize.toast(response.data ,5000,'green accent-4');
        $('#list_quotes_pagination li').removeClass('active');
        $(self).addClass('active');
    });
    request.fail(function(jqXHR, textStatus) {
        Materialize.toast(jqXHR.responseText || "Form submit failed. Please check network." ,5000,'red accent-4');
    });
};