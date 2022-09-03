
from django.urls import re_path
from .import views


app_name = "renewal"

urlpatterns = [
    re_path(r'^/', views.RenewalView.as_view(), name="renewal_post"),
]
