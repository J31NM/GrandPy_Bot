
$(document).ready(function() {
    $("#search").click(function(event) {
        event.preventDefault()
        var query = $("#query").val()
        createTextElement(query)
        // alert($("#query").val())
        var searchReq = $.getJSON("/sendRequest/", {"query": query});
        searchReq.done(onResponse);
    return true
    });
});

var mapcounter = 0

/*  */
function createMapElement() {
    var mapID = 'map' + mapcounter;
    $("#chat").append('<div id="' + mapID +'" class="map_test" ></div>');
    mapcounter ++;
    return mapID
}

function createTextElement(text) {
    $("#chat").append('<div id="papy_text" class="papy_text">' + text + '</div>');
}

function onResponse(data) {
    var coordinates = data.coordinates
    // $("#url").attr("href", data.result);
    initMap(coordinates.lat, coordinates.lng)
    createTextElement(data.response)
}

/* display a googlemap with 2 variables lat and lon */
function initMap(lat, lng) {
    if (lat === undefined){
        lat = 48.858093
    }
    if (lng === undefined){
        lng = 2.294694
    }
  var location = {lat: parseFloat(lat), lng: parseFloat(lng)};
  var mapID = createMapElement();
  var map = new google.maps.Map(
      document.getElementById(mapID), {zoom: 11, center: location});
  var marker = new google.maps.Marker({position: location, map: map});
}

