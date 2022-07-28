from django.urls import re_path, path
from .import views
from insurance import settings
from django.conf.urls.static import static

app_name = 'subcategory'

urlpatterns = [

    re_path(r'^list/',views.SubCategoryListView.as_view(),name="list"),
    re_path(r'^create/',views.SubCategoryCreate.as_view(),name="create"),
    re_path(r'^(?P<pk>[-\d]+)/delete/', views.DeleteSubCategoryView.as_view(), name = 'delete'),
    re_path(r'^(?P<pk>[-\d]+)/edit/',views.SubCategoryUpdate.as_view(),name="update"),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

