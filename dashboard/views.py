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
User = get_user_model()



class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard/home.html'



class ResetPasswordView(TemplateView):
    template_name = 'dashboard/reset-password.html'
    title = 'تغییر رمز عبور'




class PostListView(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'dashboard/blog/list.html'
    paginate_by = 10

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










