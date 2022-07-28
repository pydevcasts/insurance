
from django.contrib import admin
from django.urls import re_path
from location import views as map_views

app_name = "location"


urlpatterns = [
    re_path(r'^map/', map_views.index, name = "map"),
  
]
