/* Knobs */

// Offset Knobs
$(".offsetKnob").knob({
    'width': "150",
    'cursor': 30,
    'bgColor': "#48120E",
    'fgColor': "#E7CC8F",
    'thickness': 0.3,
    'angleArc': 250,
    'angleOffset': -125,
    'min': -50,
    'max':  50,
    'height':150,
    'change' : function(value) {
        knobClickHandler(this.$.attr('id'), (value+50)/100.0)
    },
});

// Width Knobs
$(".widthKnob").knob({
    'width': "150",
    'cursor': 30,
    'bgColor': "#48120E",
    'fgColor': "#E7CC8F",
    'thickness': 0.3,
    'angleArc': 250,
    'angleOffset': -125,
    'min': 0,
    'max': 100,
    'height':150,
    'change' : function(value) {
        knobClickHandler(this.$.attr('id'), (value)/100.0)
    },
});    

// Mute Button
$(".muteButton").click(function(){
    knobClickHandler($(this).attr("id"), $(this).prop("checked") )
})

// On click event handler
var knobClickHandler = function(id, val){
    $.post('/set_control', {
        "control": id,
        "val": val
    })
}

// Tare Button
$("#tare").click(function(){
    $.getJSON( "/orientation", function(data) {
        for(var axis in data){
            $("#"+axis+"Offset")
            .val(100*(data[axis]-0.5)+"%")
            .trigger('change')
        }
    })
})


/* Freeze Modes */
var deepFreezeButton = $('#deepFreeze')
var freezeButton = $('#freeze')

// Freeze Button
freezeButton.click(function(){
    if (freezeButton.prop('checked')){
        set_mode("freeze")
    }
    else{
        set_mode("stream")
    }
})

// Deep Freeze Button
deepFreezeButton.click(function(){
    // Only works during freeze
    if (mode == "deep_freeze")
    {
        set_mode("stream")
    }
    if (freezeButton.prop('checked'))
    {
        $.get("/set_deep_freeze").always(function(){
            set_mode("deep_freeze")
        })            
    }
    else if (deepFreezeButton.prop('checked'))
    {
        set_mode("deep_freeze")
    }
    else
    {
        set_mode("stream")
    }
})

var mode = "stream"

// Map Button
var map_return_mode = mode
var mapButton = $("#map")
mapButton.click(function(){
    map_mode = $(this).html()
    
    if(map_mode=="map")
    {
        map_return_mode = mode
    }

    set_mode("freeze", function(){
        switch(map_mode)
        {
            case "map":
                new_text = "pitch"
                break

            case "pitch":
                map_axis("pitch")
                new_text = "yaw"
                break

            case "yaw":
                map_axis("yaw")
                new_text = "roll"
                break

            case "roll":
                map_axis("roll").done(function(){set_mode(map_return_mode)})
                new_text = "map"                        
                break

            default:
                new Error("Unknown map")
        }

        $("#map").html(new_text)
    })            
})

// Update server on a mode change
var set_mode = function(new_mode, handler){
    if (handler === undefined)
    {
        handler=function(){};
    }


    $.post("/set_mode", {"mode": new_mode}).always(handler)

    // Update frontend
    switch(new_mode){
        case "freeze":
            freezeButton.prop('checked', true)
            deepFreezeButton.prop('checked', false)
            break;

        case "stream":
            freezeButton.prop('checked', false)
            deepFreezeButton.prop('checked', false)
            mapButton.html("map")
            break;

        case "deep_freeze":
            deepFreezeButton.prop('checked', true)
            freezeButton.prop('checked', true)
            break;
    }

    mode = new_mode
}

set_mode("stream")


var map_axis = function(axis){
    return $.post('/map', {"axis": axis})
}

// Pitch/Yaw/Roll Meters
setInterval(function(){
    $.getJSON( "/orientation", function(data) {
        for(var axis in data){
            $('#'+axis+"Bar")
            .css("width", 100*data[axis]+"%")
            .html(axis + "(" + Math.round(100*data[axis]-50)+"%" + ")")
        }
    })
}, 1000/20.0);

