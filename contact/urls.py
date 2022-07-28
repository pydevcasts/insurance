from django.urls import re_path
from .import views
from insurance import settings
from django.conf.urls.static import static

app_name = 'contact'

urlpatterns = [
    re_path(r'^list/', views.ListContactView.as_view(), name = 'list'), 
    re_path(r'^create/', views.CreateContactView.as_view(), name = 'create'), 
    re_path(r'^(?P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12})/delete/', views.DeleteContactView.as_view(), name = 'delete'),
    re_path(r'^(?P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12})/show/', views.ContactShowView.as_view(), name='show'),

]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)