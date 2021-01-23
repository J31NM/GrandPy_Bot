let loadingGif = document.getElementById("loading");

$( window ).on( "load", function() {
    var text = greetings()
    setInterval(createTextElement(text), 5000);
});

$(document).ready(function() {
    // document on load
    $("#search").click(function(event) {
        event.preventDefault()
        var query = $("#query").val()
        createTextElement(query, 1)
        loadingGif.hidden = false;
        // alert($("#query").val())
        var searchReq = $.getJSON("/sendRequest/", {"query": query});
        searchReq.done(onResponse);
    return true
    });
});

var mapcounter = 0

function greetings() {
        var examples = [
            "Salut fiston ! Ca faisait longtemps...... De quoi veux tu parler ?",
             "Tiens mais qui voici ? tu es venu rançonner papy ? ",
             "Qui êtes vous ? que me voulez vous ?",
             "Papy a eu plusieurs vies, il sait tout ! essaie de me coller !"
        ];
        var example = examples[Math.floor(Math.random() * examples.length)];
        return example
    }

function createMapElement() {
    var mapID = 'map' + mapcounter;
    if (mapcounter === 0) {
        mapcounter ++;
        return
    } else {
        $("#chat").append('<div id="' + mapID +'" class="map_test" ></div>');
        mapcounter ++;
        return mapID
    }

}

function createTextElement(text, i=0) {
    if (i===1) {
        $("#chat").append('<div id="user_text" class="user_text">' + text + '</div>');
    } else {
        $("#chat").append('<div id="papy_text" class="papy_text">' + text + '</div>');
    }

}

function onResponse(data) {
    console.log(data);
    var coordinates = data.coordinates
    var address = data.coordinates.address
    var answer = data.answer
    var error = data.error_message
    var text = data.text
    if (error || text == null) {
        createTextElement(error);
    } else {
        setTimeout(createTextElement(answer), 3000);
        createTextElement(text.grandPy_knowledge);
        createTextElement("Et ça se situe à cette adresse : " + address);
        initMap(coordinates.coordinates.lat, coordinates.coordinates.lng);
    }
    loadingGif.hidden = true;
}

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
      document.getElementById(mapID), {zoom: 12, center: location});
  var marker = new google.maps.Marker({position: location, map: map});
  console.log(marker);
}


