from .import views
from django.urls import re_path,path
from django.urls import path
from .views import send_notification
from django.views.generic import TemplateView

urlpatterns = [
    path('user/<int:user_id>/send_notification/', send_notification, name = 'send_notification'), 
    
]
   