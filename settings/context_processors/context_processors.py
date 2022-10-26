

from aboutus import views
from aboutus.models import About
from category.models import Category
from blog.models import Post
from news.models import New
from slider.models import Slider
from django.contrib.auth import get_user_model
from search.documents import PostDocument
from elasticsearch_dsl import Q
from team.models import Member, Team
User = get_user_model()

from django.db.models import Count
from django.utils import timezone
from datetime import timedelta


def posts_view_context_processor(request):
    setting = About.objects.filter(status = 1)
    users = User.objects.filter(email = "test@gmail.com", is_active = True, is_superuser = True)
    sliders = Slider.condition.filter(status = 1)
    members= Member.objects.select_related('team').filter(status = 1).order_by('published_at')
    teams = Team.objects.filter(status = 1).order_by('published_at')
    d = timezone.now() - timedelta(days=2)
    favorites = New.objects.annotate(
        total_views=Count('views')
                    ).filter(
                        published_at__gte=d, total_views__gt=0
                    ).order_by('-total_views')[:5]
    
    archives = New.objects.filter(status = 1).order_by('-published_at')[:8]
    categories = Category.objects.all().filter(status = "1")
    news = New.objects.filter(status = 1).order_by('-published_at')
    q = request.GET.get("q")
    if q:
        searchs = PostDocument.search().query((Q("multi_match", query=q, fields=['title', 'summary', 'content'])))
        searchs = searchs.exclude('match', draft=True) 
   
    else:
        searchs = ""    
    return ({'news':news,'archives':archives, 'favorites':favorites, 'setting':setting, 'users':users, 'sliders':sliders, 'members': members, 'teams':teams, "categories":categories, "searchs":searchs, 'title':"جستجو"  })

