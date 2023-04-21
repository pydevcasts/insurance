from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.urls import path, re_path

from . import views
from .sitemaps import NewSitemap, StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'new':NewSitemap
}

app_name = 'new'

urlpatterns = [
    re_path(r'^$', views.NewListView.as_view(), name = 'list_news'), 
    re_path(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]+)/(?P<day>[0-9]+)/(?P<slug>[\w-]+)/$', views.new_detail, name = 'detail_news'), 
    re_path(r'^sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
   