
from django.urls import re_path
from .import views
from django.conf.urls.static import static
from django.conf import settings


app_name = "frontend"
urlpatterns = [

    re_path(r'^frontend/', views.post_subcategory_list, name="post_and_subcategory"),
    re_path(r'^(?P<slug>[-\w]+)/$', views.post_subcategory_list, name='detail_by_subcategory_slug'),
    re_path(r'^frontend/.*\.*', views.pages, name='pages'),
 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                            document_root=settings.MEDIA_ROOT)