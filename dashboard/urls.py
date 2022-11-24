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
    re_path(r'^password/$', 
        views.ChangePasswordView.as_view(),name='password_change'),
    
    re_path(r'^list-post/$', views.PostListView.as_view(), name = 'post-list'), 
    re_path(r'^create-post/$', views.PostCreateView.as_view(), name = 'post-create'), 
    re_path(r'^(?P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12})/delete-post/$', views.PostDeleteView.as_view(), name = 'post-delete'),
    re_path(r'^(?P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12})/edit-post/$', views.PostUpdateView.as_view(), name='post-update'),
    re_path(r'^list-news/$', views.NewListView.as_view(), name = 'new-list'), 
    re_path(r'^create-news/$', views.NewCreateView.as_view(), name = 'new-create'), 
    re_path(r'^(?P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12})/delete-new/$', views.NewDeleteView.as_view(), name = 'new-delete'),
    re_path(r'^(?P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12})/edit-new/$', views.NewUpdateView.as_view(), name='new-update'),
    re_path(r'^sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

]
