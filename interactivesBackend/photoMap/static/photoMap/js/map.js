// helper ajax request function
var getData = function(url4, callback) {
  $.ajax({
    type: "GET",
    url: url4,
    crossDomain: true,
    dataType: "jsonp",
    data: {'format': 'jsonp'},
    success: callback
  });
}

// set default event image
var defaultImage;

var myIcon;

var map;

var placeEvent = function(event) {
  // add event marker to map
  L.marker([event.latitude,event.longitude], {icon: myIcon})
  .addEventListener("click", getEvent, {id: event.id})
  .addTo(map);

  // set default image for bottom scroll
  var eventImage = event.image;
  if (eventImage === null) {
    eventImage = defaultImage;
  };

  var startingDate = new Date(event.date);
  var endingDate = new Date(event.endDate);

  // add event to bottom scroll
  var eventBox = $("<li/>", { "class": "event",}).bind("click", function() { getEvent.call({id: event.id}); } );
  eventBox.append("<a href=#><div class='event-box' style='background-image: url(" + eventImage + ")' /><h2>" + event.name + "<br>" + $.format.date(event.date, "MMM d") + "</h2></a>");
  $("#event-scroll").append(eventBox);
}


var getEvent = function() {
  pathArray = location.href.split( '/' );
  protocol = pathArray[0];
  host = pathArray[2];
  url = protocol + '//' + host;
  getData(url + "/photoMap/api/events/" + this.id, populateOverlay);
}

var populateOverlay = function(event) {
  // set default image
  var eventImage = event.image;
  if (eventImage === null) {
    var eventImage = defaultImage;
  };

  // if it's only one day, just put the date once
  var startingDate = new Date(event.date);
  var endingDate = new Date(event.endDate);

  if (startingDate.getYear() === endingDate.getYear() && startingDate.getMonth() === endingDate.getMonth() && startingDate.getDay() === endingDate.getDay()) {
    var date = $.format.date(event.date, "MMM d");
  } else {
    var date = $.format.date(event.date, "MMM d") + " to " + $.format.date(event.endDate, "MMM d");
  };

  // populate overlay
//    $("#eventImg").html("<img src=" + eventImage + ">");
  $("#overlay-box")
    .css("background-image", "url(" + eventImage + ")");
  $("#eventName").html(event.name);
  $("#eventDate").html(date);
  $("#eventDesc").html(event.description);

  $("#overlay").fadeToggle("fast");
  $("#fade-bg").fadeToggle("fast");

}

var populateMap = function(d) {
  defaultImage = d.default_image

  // replace titles
  $("#interactive-title").html(d.name);
  document.title = d.name;

  $("#event-scroll").empty();

  d.events.sort(function(a, b) {
    return Date.parse(a.date) - Date.parse(b.date);
  });

  // populate map and bottom scroll w/ markers
  for (var i = 0; i < d.events.length; i++) {
    placeEvent(d.events[i]);
  }
};

$(window).load(function () {

  // set map's max bounds
  var cornerSW = L.latLng(51.0000,-128.0000),
      cornerNE = L.latLng(22.0000,-68.0000),
      bounds = L.latLngBounds(cornerSW, cornerNE);

  map = L.map('map', {
    zoomControl: false,
    layers: MQ.mapLayer(),
    maxBounds: bounds,
    minZoom: 4,
    maxZoom: 9,
  }).setView([39.50,-98.35], 4);

 // move zoom controls to top right
  new L.Control.Zoom({
    position: 'topright'
  }).addTo(map);

  // markers
  myIcon = L.icon({
    iconUrl: 'http://cdn.leafletjs.com/leaflet-0.7.3/images/marker-icon.png',
    iconRetinaUrl: 'http://cdn.leafletjs.com/leaflet-0.7.3/images/marker-icon-2x.png',
    iconSize: [25, 41],
    iconAnchor: [12, 40],
    shadowUrl: 'http://cdn.leafletjs.com/leaflet-0.7.3/images/marker-shadow.png',
    shadowRetinaUrl: 'http://cdn.leafletjs.com/leaflet-0.7.3/images/marker-shadow.png',
    shadowSize: [41, 41],
    shadowAnchor: [12, 40]
  }); 

  $("#attribution-overlay").hide();
  $("#attr-fade-bg").hide();
  $("#overlay").hide();
  $("#fade-bg").hide();
  $("#exit-button").click(function() {
    $("#overlay").fadeToggle("fast");
    $("#fade-bg").fadeToggle("fast");
  });

  $("#fade-bg").click(function() {
    $("#overlay").fadeToggle("fast");
    $("#fade-bg").fadeToggle("fast");
  });

  $("#attribution-link").click(function() {
    $("#attribution-overlay").fadeToggle("fast");
    $("#attr-fade-bg").fadeToggle("fast");
  });

  $("#attr-exit-button").click(function() {
    $("#attribution-overlay").fadeToggle("fast");
    $("#attr-fade-bg").fadeToggle("fast");
  });

  $("#attr-fade-bg").click(function() {
    $("#attribution-overlay").fadeToggle("fast");
    $("#attr-fade-bg").fadeToggle("fast");
  });

});