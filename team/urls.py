

from django.urls import re_path

from team.views import TeamView

app_name = "team"

urlpatterns = [
    re_path(r'^', TeamView.as_view(), name = "team-insurance"), 
  
]