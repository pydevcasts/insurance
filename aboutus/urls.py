
from django.urls import re_path

from aboutus.views import AboutView

app_name = "about"

urlpatterns = [
    re_path(r'^', AboutView.as_view(), name = "about-insurance"), 
  
]