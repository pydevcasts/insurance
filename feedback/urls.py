from .import views
from django.urls import re_path
from django.conf import settings
from django.conf.urls.static import static



app_name = 'customer-feedback'

urlpatterns = [
    re_path(r'^', views.CustomerFeedbackListView.as_view(), name = 'list'), 
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
   