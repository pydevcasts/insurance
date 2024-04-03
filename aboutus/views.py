
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import ListView

from aboutus.models import About


@method_decorator(cache_page(60 * 60 * 24), name='dispatch')
class AboutView(ListView):
    model = About
    context_object_name = 'abouts'
    template_name = 'frontend/about/index.html'
   
    def get_queryset(self):
        return super().get_queryset().filter(status = 1)


    def get_context_data(self, **kwargs):
        title = "درباره ما"
        context = super().get_context_data(**kwargs)
        context['title'] = title
        return context





