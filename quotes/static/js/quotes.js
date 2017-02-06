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
});