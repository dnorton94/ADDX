// Thanks: http://jsfiddle.net/39ZvN/9/

$(function() {
    var oldList, newList, item;
    $('.sortable').sortable({
        start: function(event, ui) {
            item = ui.item;
            newList = oldList = ui.item.parent().parent();
        },
        stop: function(event, ui) {   
            // TODO: update server       
            //alert("Moved " + item.text() + " from " + oldList.attr('id') + " to " + newList.attr('id'));
        },
        change: function(event, ui) {  
            if(ui.sender) newList = ui.placeholder.parent().parent();
        },
        connectWith: ".sortable"
    }).disableSelection();
});