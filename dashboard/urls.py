from django.urls import re_path
from .import views
from django.contrib.auth import views as auth_views


app_name = 'dashboard'
urlpatterns = [
    re_path(r'home/',views.DashboardView.as_view(), name = 'home'), 
    re_path(r'^settings/password/$', 
        auth_views.PasswordChangeView.as_view(template_name='backend/accounts/password_change.html'),
        name='password_change'),
    
    
]
