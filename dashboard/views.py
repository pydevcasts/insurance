from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models.query_utils import Q
from django.shortcuts import redirect
from django.urls.base import reverse_lazy
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from blog.models import Post
from blog.forms import PostForm
from news.models import New
from news.forms import NewForm
User = get_user_model()
from django.contrib.auth.views import PasswordChangeView



class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard/home.html'

    def get_context_data(self, **kwargs):
        return {'segment':'داشبورد بیمه'}



class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name='dashboard/accounts/password_change.html'
    success_message = "پسوردتان با موفقیت تغیرر یافت"
    success_url = reverse_lazy('dashboard:password_change')
   
  



class PostListView(PermissionRequiredMixin,LoginRequiredMixin, ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'dashboard/blog/list.html'
    paginate_by = 10
    permission_required = "post.view_post"

    def handle_no_permission(self):
        messages.warning(
            self.request, " شما اجازه دسترسی به این صفحه رو ندارید")
        return redirect("dashboard:home")


    # it is for pagination
    def get_queryset(self):
        filter_val = self.request.GET.get("filter", "")
        order_by = self.request.GET.get("orderby", "pk")
        if filter_val != "":
            post = Post.objects.filter(Q(title__contains=filter_val) | Q(
                description__contains=filter_val)).order_by(order_by)
        else:
            post = Post.objects.all().order_by(order_by)
        return post


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = self.request.GET.get("filter", "")
        context["orderby"] = self.request.GET.get("orderby", "pk")
        context["all_table_fields"] = Post._meta.get_fields()
        context['segment'] = "لیست پست"
        return context


class PostCreateView(SuccessMessageMixin, PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    context_object_name = "form"
    template_name = "dashboard/blog/create.html"
    success_url = reverse_lazy('dashboard:post-list')
    success_message = "پست با موفقیت ایجاد شد !"
    permission_required = "post.create_post"

    def handle_no_permission(self):
        messages.warning(
            self.request, " شما اجازه دسترسی به این صفحه رو ندارید")
        return redirect("dashboard:home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "ایجاد پست"
        return context
    
  


class PostDeleteView(SuccessMessageMixin, PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Post
    permission_required = "post.delete_post"
    template_name = 'dashboard/blog/list.html'
    success_url = reverse_lazy('dashboard:post-list')


    def handle_no_permission(self):
        messages.warning(
            self.request, " شما اجازه دسترسی به این صفحه رو ندارید")
        return redirect("dashboard:home")

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        if pk is not None:
            post_object = Post.objects.get_queryset().filter(pk=pk)
            if post_object is not None:
                post_object.delete()
                messages.success(request, "پست با موفقیت حذف گردید!")
                return redirect('dashboard:post-list')
        return redirect('dashboard/blog/list.html')


class PostUpdateView(SuccessMessageMixin, PermissionRequiredMixin,LoginRequiredMixin, UpdateView):

    form_class = PostForm
    model = Post
    permission_required = "post.update_post"
    pk_url_kwarg = 'pk'
    template_name = 'dashboard/blog/edit.html'
    success_url = reverse_lazy('dashboard:post-list')
    success_message = "پست با موفقیت ویرایش گردید!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "ویرایش پست"
        return context
    
    def handle_no_permission(self):
        messages.warning(
            self.request, " شما اجازه دسترسی به این صفحه رو ندارید")
        return redirect("dashboard:home")






# =======================================
#  ##############داشبورد###############
# =======================================


class NewListView(PermissionRequiredMixin,LoginRequiredMixin, ListView):
    model = New
    context_object_name = 'news'
    template_name = 'dashboard/news/list.html'
    paginate_by = 10
    permission_required = "new.view_news"

    def handle_no_permission(self):
        messages.warning(
            self.request, " شما اجازه دسترسی به این صفحه رو ندارید")
        return redirect("dashboard:home")

    # it is for pagination
    def get_queryset(self):
        filter_val = self.request.GET.get("filter", "")
        order_by = self.request.GET.get("orderby", "pk")
        if filter_val != "":
            new = New.objects.filter(Q(title__contains=filter_val) | Q(
                description__contains=filter_val)).order_by(order_by)
        else:
            new = New.objects.all().order_by(order_by)
        return new


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = self.request.GET.get("filter", "")
        context["orderby"] = self.request.GET.get("orderby", "pk")
        context["all_table_fields"] = New._meta.get_fields()
        context['segment'] = "لیست خبر"
        return context


class NewCreateView(SuccessMessageMixin, PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = New
    form_class = NewForm
    context_object_name = "form"
    template_name = "dashboard/news/create.html"
    success_url = reverse_lazy('dashboard:new-list')
    success_message = "خبر با موفقیت ایجاد شد !"
    permission_required = "new.create_news"

    def handle_no_permission(self):
        messages.warning(
            self.request, " شما اجازه دسترسی به این صفحه رو ندارید")
        return redirect("dashboard:home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "ایجاد خبر"
        return context
    
  


class NewDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = New
    permission_required = "new.delete_post"
    template_name = 'dashboard/news/list.html'
    success_url = reverse_lazy('dashboard:new-list')


    def handle_no_permission(self):
        messages.warning(
            self.request, " شما اجازه دسترسی به این صفحه رو ندارید")
        return redirect("dashboard:home")

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        if pk is not None:
            post_object = New.objects.get_queryset().filter(pk=pk)
            if post_object is not None:
                post_object.delete()
                messages.success(request, "خبر با موفقیت حذف گردید!")
                return redirect('dashboard:new-list')
        return redirect('dashboard/new/list.html')


class NewUpdateView(SuccessMessageMixin, PermissionRequiredMixin,LoginRequiredMixin, UpdateView):

    form_class = NewForm
    model = New
    permission_required = "new.update_new"
    pk_url_kwarg = 'pk'
    template_name = 'dashboard/news/edit.html'
    success_url = reverse_lazy('dashboard:new-list')
    success_message = "خبر با موفقیت ویرایش گردید!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "ویرایش خبر"
        return context
    
    def handle_no_permission(self):
        messages.warning(
            self.request, " شما اجازه دسترسی به این صفحه رو ندارید")
        return redirect("dashboard:home")



