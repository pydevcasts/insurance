

from django.contrib import messages
from django.urls.base import reverse_lazy
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from blog.models import Post
from category.models import Category
from category.forms import CategoryForm
from django.db.models import Q
from django.shortcuts import get_object_or_404, render,redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt



class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'dashboard/category/list.html'
    paginate_by=15
    
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
        context['segment'] = "لیست دسته بندی"
        return context


@method_decorator(csrf_exempt, name='dispatch')
class CreateCategoryView(SuccessMessageMixin, PermissionRequiredMixin,LoginRequiredMixin, CreateView):
    model = Category
    permission_required = "category.create_category"
    template_name = 'dashboard/category/create.html'
    form_class = CategoryForm
    success_url = reverse_lazy('category:cat-list')
    success_message = "دسته بندی با موفقیت ایجاد گردید!"

    def handle_no_permission(self):
        messages.warning(self.request, " شما اجازه دسترسی به این صفحه رو ندارید")
        return redirect("dashboard:home")

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['segment'] = "ایجاد دسته بندی"
        return context


@method_decorator(csrf_exempt, name='dispatch')
class DeleteCategoryView(SuccessMessageMixin, PermissionRequiredMixin, LoginRequiredMixin,DeleteView):
    model = Category
    permission_required = "category.delete_category"
    template_name = 'dashboard/category/list.html'
    success_url = reverse_lazy('category:cat-list')
   

    def handle_no_permission(self):
        messages.warning(self.request, " شما اجازه دسترسی به این صفحه رو ندارید")
        return redirect("dashboard:home")
    
    def get(self, request, *args, **kwargs):
        pk=kwargs.get("pk")
        if pk is not None:
            category_object = Category.objects.get_queryset().get(pk= pk)
            if category_object is not None:
                category_object.delete()
                messages.success(request, "دسته بندی شما با موفقیت حذف گردید!")
                return redirect('category:cat-list')
        return redirect('dashboard/category/list.html')



@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(SuccessMessageMixin, PermissionRequiredMixin,LoginRequiredMixin, UpdateView):
    model = Category
    template_name = 'dashboard/category/edit.html'
    form_class = CategoryForm
    pk_url_kwarg = 'pk'
    success_message="دسته بندی با موفقیت ویرایش شد!"
    success_url = reverse_lazy('category:cat-list')
    permission_required = "category.update_category"


    def handle_no_permission(self):
        messages.warning(self.request, " شما اجازه دسترسی به این صفحه رو ندارید")
        return redirect("dashboard:home")


@csrf_exempt
def posts_list_by_category(request, slug=None, *args, **kwargs):

    category = None
    posts = Post.objects.filter(status=1)
    if slug:
        category = get_object_or_404(Category, slug=slug)
        posts = posts.filter(category=category)
        page = request.GET.get('page', 1)

        paginator = Paginator(posts, 15)
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
    return render(request,
                  'frontend/posts/list_category.html',
                  {'page_obj':page_obj, 'title':'دسته بندی ها','segment':'دسته بندی '})


