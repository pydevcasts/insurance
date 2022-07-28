
from django.contrib import admin
from django.urls import re_path, include
from search import views as search_view



urlpatterns  = [
    re_path(r'^', search_view.search_post, name = "search-post"),
  
    
]