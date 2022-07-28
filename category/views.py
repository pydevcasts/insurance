

from django.contrib.messages.api import success
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls.base import reverse, reverse_lazy
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from category.models import Category, SubCategory
from category.forms import CategoryForm, SubCategoryForm
from django.db.models import Q
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


# @method_decorator(cache_page(60 * 60 * 24), name='dispatch')
class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'backend/category/list.html'
    paginate_by=10
    
    # it is for pagination
    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            cat=Category.objects.filter(Q(title__contains=filter_val) | Q(description__contains=filter_val)).order_by(order_by)
        else:
            cat=Category.objects.all().order_by(order_by)

        return cat

    def get_context_data(self,**kwargs):
        context=super(CategoryListView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=Category._meta.get_fields()
        return context



class CreateCategoryView(SuccessMessageMixin, PermissionRequiredMixin,LoginRequiredMixin, CreateView):
    model = Category
    permission_required = "category.create_category"
    template_name = 'backend/category/create.html'
    form_class = CategoryForm
    success_url = reverse_lazy('category:list')
    success_message = "Category Create successfully"

    def handle_no_permission(self):
        messages.warning(self.request, "You dont have permission to this page please signin with superuser!")
        return redirect("dashboard:home")


class DeleteCategoryView(SuccessMessageMixin, PermissionRequiredMixin, DeleteView):
    model = Category
    permission_required = "category.delete_category"
    template_name = 'backend/category/list.html'
    pk_url_kwarg = 'slug'
    success_url = reverse_lazy('category:list')
    success_message = "Category Delete successfully"

    def handle_no_permission(self):
        messages.warning(self.request, "You dont have permission to this page please signin with superuser!")
        return redirect("dashboard:home")
    
    def get(self, request, *args, **kwargs):
        pk=kwargs.get("pk")
        if pk is not None:
            category_object = Category.objects.get_queryset().get(pk= pk)
            if category_object is not None:
                category_object.delete()
                messages.success(request, 'Category is deleted successfully.') 
                return redirect('category:list')
        return redirect('backend/category/list.html')
       

class CategoryUpdateView(SuccessMessageMixin, UpdateView):
    model = Category
    template_name = 'backend/category/edit.html'
    pk_url_kwarg = 'pk'
    fields = "__all__" 
    success_message="Category Updated!"
    success_url = reverse_lazy('category:list')

    def handle_no_permission(self):
        messages.warning(self.request, "You dont have permission to this page please signin with superuser!")
        return redirect("dashboard:home")

# subcat
# @method_decorator(cache_page(60 * 60 * 24), name='dispatch')
class SubCategoryListView(ListView):
    model=SubCategory
    paginate_by=3
    context_object_name = "subcategories"
    template_name="backend/subcategory/list.html"

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            cat=SubCategory.objects.filter(Q(title__contains=filter_val) | Q(description__contains=filter_val)).order_by(order_by)
        else:
            cat=SubCategory.objects.all().order_by(order_by)
        return cat

    def get_context_data(self,**kwargs):
        context=super(SubCategoryListView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=SubCategory._meta.get_fields()
        return context



class SubCategoryCreate(SuccessMessageMixin,PermissionRequiredMixin, CreateView):
    model=SubCategory
    form_class = SubCategoryForm
    permission_required = "subcategory.create_subcategory"
    success_message="Sub Category Added!"
    template_name="backend/subcategory/create.html"
    success_url = reverse_lazy('subcategory:list')


    def handle_no_permission(self):
        messages.warning(self.request, "You dont have permission to this page please signin with superuser!")
        return redirect("dashboard:home")
    
  

class SubCategoryUpdate(SuccessMessageMixin,UpdateView):
    model=SubCategory
    fields="__all__"
    success_message="Sub Category Updated!"
    template_name="backend/subcategory/edit.html"
    success_url = reverse_lazy('subcategory:list')

    def handle_no_permission(self):
        messages.warning(self.request, "You dont have permission to this page please signin with superuser!")
        return redirect("dashboard:home")

class DeleteSubCategoryView(SuccessMessageMixin, DeleteView):
    model = SubCategory
    template_name = 'backend/subcategory/list.html'
    success_url = reverse_lazy('subcategory:list')
    success_message = "Category Delete successfully"

    def handle_no_permission(self):
        messages.warning(self.request, "You dont have permission to this page please signin with superuser!")
        return redirect("dashboard:home")
    
    def get(self, request, *args, **kwargs):
        pk=kwargs.get("pk")
        if pk is not None:
            category_object = SubCategory.objects.get_queryset().get(pk= pk)
            if category_object is not None:
                category_object.delete()
                messages.success(request, 'Category is deleted successfully.') 
                return redirect('subcategory:list')
        return redirect('backend/subcategory/list.html')
       