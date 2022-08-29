
from django.urls import re_path,path
from .import views
from django.conf.urls.static import static
from django.conf import settings


app_name = "frontend"
urlpatterns = [

    re_path(r'^insurance/', views.post_subcategory_list, name="post_and_subcategory"),
    re_path(r'^insurance/(?P<slug>[-\w]+)/$', views.post_subcategory_list, name='detail_by_subcategory_slug'),
    re_path(r'^insurance/.*\.*', views.pages, name='pages'),
    path('mail/newsletter/unsubscribe/<str:token>', views.unsubscrib_redirect_view, name = "unsubscribe_redirect"),
    re_path(r'^(?P<slug>[-\w]+)/detail/$', views.PostDetailView.as_view(), name = 'detail'),
    # re_path(r'^mail/newsletter/unsubscribe/(?P<token>[0-9A-Za-z].[0-9A-Za-z].[0-9A-Za-z])', views.unsubscrib_redirect_view, name = "unsubscribe_redirect"),
    # [A-Za-z0-9.-]

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                            document_root=settings.MEDIA_ROOT)
