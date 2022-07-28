from .import views
from django.urls import re_path, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap 
from blog.sitemaps import StaticViewSitemap,PostSitemap
sitemaps = {
    'static': StaticViewSitemap,
    'post':PostSitemap
}

app_name = 'blog'

urlpatterns = [
    re_path(r'^list/$', views.PostListView.as_view(), name = 'list'), 
    re_path(r'^create/$', views.PostCreateView.as_view(), name = 'create'), 
    re_path(r'^(?P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12})/delete/$', views.PostDeleteView.as_view(), name = 'delete'),
    re_path(r'^(?P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12})/edit/$', views.PostUpdateView.as_view(), name='update'),
    re_path(r'^(?P<slug>[-\w]+)/detail/$', views.PostDetailView.as_view(), name = 'detail'),
    re_path(r'^sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
   