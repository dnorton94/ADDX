// Thanks: http://jsfiddle.net/39ZvN/9/

$(function() {
    var oldList, newList, item;
    $('.sortable').sortable({
        start: function(event, ui) {
            item = ui.item;
            newList = oldList = ui.item.parent().parent();
        },
        stop: function(event, ui) {
            var inventory = []
            $("#inventory").children('li').each(function(i, elem) {
                inventory.push($(elem).text());
            });

            $.post("/inventoryUpdate", {
                "inventory": inventory
            }, 
            function(response_data){
                console.log(response_data);
            })
            // TODO: update server       
            //alert("Moved " + item.text() + " from " + oldList.attr('id') + " to " + newList.attr('id'));
        },
        change: function(event, ui) {  
            if(ui.sender) newList = ui.placeholder.parent().parent();
        },
        connectWith: ".sortable"
    }).disableSelection();
});