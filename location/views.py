from django.shortcuts import render
import folium
import geocoder
from location.models import Location


def index(request):
    address = Location.objects.all().last()
    location = geocoder.osm(address)
    lat = location.lat
    lng = location.lng
    country = location.country
    map = folium.Map(location=[19,-12], zoom_start=2)
   
    folium.Marker([lat,lng],tooltip="click for more",popup = country).add_to(map)
    map = map._repr_html_()
  
    context = {
        'map':map
    }
    return render (request, "frontend/location/map.html", context)