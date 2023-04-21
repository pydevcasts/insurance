from django.urls import re_path

from . import views

app_name = 'tag'

urlpatterns = [
    re_path(r'^list/', views.TagListView.as_view(), name = 'tag-list'), 
    re_path(r'^create/', views.CreateTagView.as_view(), name = 'tag-create'), 
    re_path(r'^(?P<slug>[-\w]+)/delete/', views.DeleteTagView.as_view(), name = 'tag-delete'),
    re_path(r'^(?P<slug>[-\w]+)/edit/', views.TagUpdateView.as_view(), name='tag-update'),
 
]
