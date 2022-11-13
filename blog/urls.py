from .import views
from django.urls import re_path, path
from django.conf import settings
from django.conf.urls.static import static


app_name = 'blog'

urlpatterns = [
   
    path('', views.post_category_list, name="post_and_category"),
    re_path(r'^insurance/(?P<slug>[-\w]+)/$', views.post_category_list, name='detail_by_category_slug'),
    re_path(r'^all_post/', views.all_post_view, name = "all_post"),
    re_path(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]+)/(?P<day>[0-9]+)/(?P<slug>[\w-]+)/$', views.PostDetailView.as_view(), name = 'detail'),
    path('mail/newsletter/unsubscribe/<str:token>', views.unsubscrib_redirect_view, name = "unsubscribe_redirect"),
   
    # re_path(r'^mail/newsletter/unsubscribe/(?P<token>[0-9A-Za-z].[0-9A-Za-z].[0-9A-Za-z])', views.unsubscrib_redirect_view, name = "unsubscribe_redirect"),
    # [A-Za-z0-9.-]

]


if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
   