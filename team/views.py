

from team.models import Team
from django.views.generic import ListView


class TeamView(ListView):
    model = Team
    template_name = 'frontend/team/index.html'


