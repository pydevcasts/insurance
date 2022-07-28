from django.urls import re_path, path
from .import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'category'

urlpatterns = [
    re_path(r'^list/', views.CategoryListView.as_view(), name = 'list'), 
    re_path(r'^create/', views.CreateCategoryView.as_view(), name = 'create'), 
    re_path(r'^(?P<pk>[-\d]+)/delete/', views.DeleteCategoryView.as_view(), name = 'delete'),
    re_path(r'^(?P<pk>[-\d]+)/edit/', views.CategoryUpdateView.as_view(), name='update'),

]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)