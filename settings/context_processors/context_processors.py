
from aboutus.models import About
from slider.models import Slider
from django.contrib.auth import get_user_model

from team.models import Member
User = get_user_model()



def posts_view_context_processor(request):
    setting = About.objects.get(status = 1)
    users = User.objects.filter(email = "test@gmail.com", is_active = True, is_superuser = True)
    sliders = Slider.objects.filter(status = 1)
    members= Member.objects.select_related('team').filter(status = 1).order_by('published_at')
  
    return ({'setting' : setting, 'users':users, 'sliders':sliders, 'members': members, })

