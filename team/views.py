

from django.views.generic import ListView

from team.models import Team


class TeamView(ListView):
    model = Team
    template_name = 'frontend/team/index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "تیم ما"
        return context


