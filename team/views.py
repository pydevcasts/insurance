
from multiprocessing import get_context
from team.models import Member, Team
from django.views.generic import ListView
from django.db.models.query_utils import Q

class TeamView(ListView):
    model = Team
    template_name = 'frontend/team/index.html'

    def get_queryset(self):
        return super().get_queryset().filter(status = 1)


    def get_context_data(self, **kwargs):
        title = "تیم ما"
        context = super().get_context_data(**kwargs)
        context['title'] = title
        context['members'] = Member.objects.select_related('team').filter(status = 1).order_by('published_at')
        return context


