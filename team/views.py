

from multiprocessing import context
from team.models import Team
from django.views.generic import ListView


class TeamView(ListView):
    model = Team
    template_name = 'frontend/team/index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "تیم ما"
        context['segemnt'] = "تیم ما"
        return context


