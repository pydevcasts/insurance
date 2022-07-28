from . import views
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static


app_name = 'tickets'

urlpatterns = [

    # create new ticket
    re_path(r'^ticket/new/$', views.ticket_create_view, name='ticket_create'),
    # edit ticket
    re_path(r'^ticket/edit/(?P<pk>\d+)/$', views.ticket_edit_view, name='ticket_edit'),
    # view ticket
    re_path(r'^ticket-detail/(?P<pk>\d+)/$', views.ticket_detail_view, name='ticket_detail'),
    # create new followup
    re_path(r'^followup/new/$', views.followup_create_view, name='followup_new'),
    # edit followup
    re_path(r'^followup/edit/(?P<pk>\d+)/$', views.followup_edit_view, name='followup_edit'),
    # create new attachment
    re_path(r'^attachment/new/$', views.attachment_create_view, name='attachment_new'),
    re_path(r'^my-tickets/$', views.my_tickets_view, name='my-tickets'),
    re_path(r'^list/$', views.all_tickets_view, name='list'),
    # re_path(r'^archive/$', views.archive_view, name='archive'),

 ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

