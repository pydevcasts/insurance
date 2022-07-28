from .import views
from django.urls import re_path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'user'

urlpatterns = [
    re_path(r'^generate/', views.GenerateRandomUserView.as_view(), name='generate'),
    re_path(r'^create/', views.ProfileView.as_view(), name='create'),
    re_path(r'^list/', views.UserListView.as_view(), name = 'list'), 
    re_path(r'^(?P<pk>[-\w]+)/delete/', views.DeleteUserView.as_view(), name = 'delete'),
 
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)