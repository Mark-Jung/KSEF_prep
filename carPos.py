# -*- coding: utf-8 -*-
def write(data,car_data):
        html_header = """<!DOCTYPE html>
        <html>
          <head>
            <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
            <meta charset="utf-8">
            <title>Suspect Position</title>
            <style>
              #map {
                height: 100%;
              }
              html, body {
                height: 100%;
                margin: 0;
                padding: 0;
              }
            </style>
          </head>
          <body>
          <div id="map"></div>
            <script>
              function initMap() {
              """
        html_footer ="""
                var latlngStr = myData.split(',', 5);		
                var map = new google.maps.Map(document.getElementById('map'), {
                  zoom: 8,
                  center: {lat: parseFloat(latlngStr[3]), lng: parseFloat(latlngStr[4])} 
                });
                var geocoder = new google.maps.Geocoder;
                var infowindow = new google.maps.InfoWindow;
                geocodeLatLng(geocoder, map, infowindow, myData);
              }
              function geocodeLatLng(geocoder, map, infowindow, myData) {
                var latlngStr = myData.split(',', 5);
                var latlng = {lat: parseFloat(latlngStr[3]), lng: parseFloat(latlngStr[4])}; 	
                geocoder.geocode({'location': latlng}, function(results, status) {
                  if (status === 'OK') {
                    if (results[1]) {
                      map.setZoom(11);
                      var marker = new google.maps.Marker({
                        position: latlng,
                        map: map
                      });
                      infowindow.setContent(latlngStr[1]+' '+latlngStr[2]+'<br>'+latlngStr[0]+'<br>'+results[1].formatted_address+'<br>'+latlngStr[3]+', '+latlngStr[4]);
                      infowindow.open(map, marker);
        	   google.maps.event.addListener(marker, 'click', function() {infowindow.open(map, marker);});
                    } else {
                      window.alert('No results found');
                    }
                  } else {
                    window.alert('Geocoder failed due to: ' + status);
                  }
                });
              }
            </script>
            <script async defer
            src="https://maps.googleapis.com/maps/api/js?key=AIzaSyBOW3CHXqjZZWEu-cZBZ5cdMn59J824ak4&callback=initMap">
            </script>
          </body>
        </html>"""

        #gpsdata=data.split(',')
        fileName = car_data[-4:]+".LOC.html"
        f = open(fileName, 'w')
        f.write(html_header)

        #f.write("var myData='"+str(car_data)+","+str(data[0])+","+str(data[1])+","+str(data[2])+","+str(data[3]).rstrip()+"';")
        f.write("var myData='"+str(car_data)+","+str(data).rstrip()+"';")

        f.write(html_footer)
        f.close()
#end def

