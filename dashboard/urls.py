from django.urls import re_path
from .import views
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap 
from dashboard.sitemaps import StaticViewSitemap,PostSitemap
sitemaps = {
    'static': StaticViewSitemap,
    'post':PostSitemap
}

app_name = 'dashboard'

urlpatterns = [
    re_path(r'home/',views.DashboardView.as_view(), name = 'home'), 
    re_path(r'^settings/password/$', 
        auth_views.PasswordChangeView.as_view(template_name='dashboard/accounts/password_change.html'),
        name='password_change'),
    
    re_path(r'^list/$', views.PostListView.as_view(), name = 'list'), 
    re_path(r'^create/$', views.PostCreateView.as_view(), name = 'create'), 
    re_path(r'^(?P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12})/delete/$', views.PostDeleteView.as_view(), name = 'delete'),
    re_path(r'^(?P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12})/edit/$', views.PostUpdateView.as_view(), name='update'),
    re_path(r'^sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]
