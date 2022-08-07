from django.urls import re_path
from .import views


app_name = 'faq'

urlpatterns = [
    re_path(r'^', views.CreateFAQView.as_view(), name = 'faq-insurance'), 

]
