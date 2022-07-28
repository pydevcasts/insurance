
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models.query_utils import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls.base import reverse_lazy
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from blog.models import Post
from tag.models import Tag
from blog.forms import PostForm
from django.utils import timezone
from category.models import Category, SubCategory
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.http.response import HttpResponse, HttpResponseRedirect
from django.template import loader
from django import template


User = get_user_model()

# @method_decorator(cache_page(60 * 60 * 24), name='dispatch')
class PostListView(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'backend/blog/list.html'
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
        context = super(PostListView, self).get_context_data(**kwargs)
        context["filter"] = self.request.GET.get("filter", "")
        context["orderby"] = self.request.GET.get("orderby", "pk")
        context["all_table_fields"] = Post._meta.get_fields()
        return context


class PostCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    context_object_name = "form"
    template_name = "backend/blog/create.html"
    success_url = reverse_lazy('blog:list')
    success_message = "Post Added Successfully!"
    permission_required = "post.create_post"

    def handle_no_permission(self):
        messages.warning(
            self.request, "You dont have permission to this page please signin with superuser!")
        return redirect("dashboard:home")

    def get(self, request, *args, **kwargs):
        categories = Category.objects.filter(status = "1")
        tags = Tag.objects.filter(status="1").order_by(
            "-created").prefetch_related('post')
        users = User.objects.all()
        categories_list = []
        for category in categories:
            sub_category = SubCategory.objects.filter(category_id=category.id)
            categories_list.append(
                {"category": category, "sub_category": sub_category})
        return render(request, "backend/blog/create.html", {"categories": categories_list, "tags": tags, 'users': users})


class PostDeleteView(SuccessMessageMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    permission_required = "post.delete_post"
    template_name = 'backend/blog/list.html'
    success_url = reverse_lazy('blog:list')
    success_message = "Post Delete successfully"

    def handle_no_permission(self):
        messages.warning(
            self.request, "You dont have permission to this page please signin with superuser!")
        return redirect("dashboard:home")

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        if pk is not None:
            post_object = Post.objects.get_queryset().filter(pk=pk)
            if post_object is not None:
                post_object.delete()
                messages.success(request, 'Your Post was updated.')
                return redirect('blog:list')
        return redirect('backend/blog/list.html')


class PostUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):

    def handle_no_permission(self):
        messages.warning(
            self.request, "You dont have permission to this page please signin with superuser!")
        return redirect("dashboard:home")

    def get(self, request, *args, **kwargs):
        post_id = kwargs['pk']
        categories = Category.objects.all()
        tags = Tag.objects.filter(status="1").order_by(
            "-created").prefetch_related('post')
        posts = Post.objects.all()
        users = User.objects.all()
        post = Post.objects.get(pk=post_id)
        categories_list = []
        for category in categories:
            sub_category = SubCategory.objects.filter(category_id=category.id)
            categories_list.append(
                {"category": category, "sub_category": sub_category})
        return render(request, "backend/blog/edit.html", {"categories": categories_list, "post": post, "tags": tags, "posts": posts, 'users': users})

    def post(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, pk=kwargs['pk'])
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES or None,
                            instance=instance)
            if form.is_valid():
                form = form.save(commit=False)
                form.user = request.user
                form.updated = timezone.now()
                form.save()
                messages.success(request,
                                 "Post updated successfull!")
                return redirect("blog:list")
        else:
            form = PostForm()
        return render(request, 'backend/blog/edit.html',
                      {'form': form}
                      )


class PostDetailView(DetailView):
    template_name = 'frontend/landing/detail.html'
    context_object_name = "post"
    model = Post

    def get_object(self, queryset=None):
        post = Post.objects.get(slug=self.kwargs.get("slug"))
        return post

