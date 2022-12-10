

from aboutus.models import About
from blog.models import Post
from category.models import Category
from news.models import New
from slider.models import Slider
from django.contrib.auth import get_user_model
from team.models import Member, Team
from django.db.models import Q
User = get_user_model()



def posts_view_context_processor(request):
    setting = About.objects.filter(status = 1)
    users = User.objects.filter(email = "siyamak1981@gmail.com", is_active = True, is_superuser = True)
    sliders = Slider.condition.filter(status = 1)
    members= Member.objects.select_related('team').filter(status = 1).order_by('published_at')
    teams = Team.objects.filter(status = 1).order_by('published_at')
    archives = New.objects.filter(status = 1).order_by('-published_at')[:8]
    categories = Category.objects.all().filter(status = "1")
   
    q = request.GET.get("q")
    if q:
        searchs = Post.objects.filter(Q(title__icontains=q) | Q(content__icontains=q) | Q(summary__icontains = q))
    else:
        searchs = ""   
 
    return ({'archives':archives, 'setting':setting, 'users':users, 'sliders':sliders, 'members': members, 'teams':teams, "categories":categories, "searchs":searchs, 'title':"جستجو"  })

