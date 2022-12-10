from django.urls import re_path
from django.contrib.auth import views as auth_views
from accounts import views as accounts_views

app_name = "accounts"
urlpatterns = [
    re_path(r'^signup/$', accounts_views.signup, name='signup'),
        ]