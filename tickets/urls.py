from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path

from . import views

app_name = 'tickets'

urlpatterns = [
    re_path(r'^ticket/create/$', views.TicketCreate.as_view(), name='ticket_create'),
    re_path(r'^update/(?P<pk>\d+)/$', views.TicketUpdate.as_view(), name='update_ticket'),
    re_path(r'^ticket-detail/(?P<pk>\d+)/$', views.ticket_detail_view, name='ticket_detail'),
    re_path(r'^ticket-followup-reply/(?P<pk>\d+)$', views.FollowupReplyView.as_view(), name='followup_reply'),
    re_path(r'^list/$', views.TicketListView.as_view(), name='ticket-list'),
    re_path(r'^delete-attach/(?P<pk>\d+)/$', views.delete_attachments, name='delete_attachments'),

 ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

