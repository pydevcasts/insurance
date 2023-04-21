from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path

from . import views

app_name = 'user'

urlpatterns = [

    re_path(r'^create/', views.ProfileView.as_view(), name='user-create'),
    re_path(r'^list/', views.UserListView.as_view(), name = 'user-list'), 
    re_path(r'^(?P<pk>[-\w]+)/delete/', views.DeleteUserView.as_view(), name = 'user-delete'),
    re_path(r'^edit/(?P<pk>[-\d]+)/$', views.ProfileUpdateView.as_view(), name='user-update'),
    re_path(r'^password-change/', views.ChangePasswordView.as_view(), name='password_change'),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)