from django.urls import re_path
from .import views


app_name = 'tag'

urlpatterns = [
    re_path(r'^list/', views.TagListView.as_view(), name = 'list'), 
    re_path(r'^create/', views.CreateTagView.as_view(), name = 'create'), 
    re_path(r'^generate/', views.GenerateRandomTagView.as_view(), name = 'random'), 
    re_path(r'^(?P<slug>[-\w]+)/delete/', views.DeleteTagView.as_view(), name = 'delete'),
    re_path(r'^(?P<slug>[-\w]+)/edit/', views.TagUpdateView.as_view(), name='update'),
    # path('<str:slug>/delete/', views.DeleteTagView.as_view(), name = 'delete'),
 
]
