
from django.contrib import messages
from django.shortcuts import redirect
from django.urls.base import  reverse_lazy
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from tag.models import Tag
from tag.forms import TagForm
from django.db.models import Q



class TagListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Tag
    context_object_name = 'tags'
    template_name = 'dashboard/tag/list.html'
    paginate_by = 20
    permission_required = "tag.view_tag"

    def handle_no_permission(self):
        messages.warning(self.request, "شما اجازه دسترسی به این صفحه رو ندارید")
        return redirect("dashboard:home")

      # it is for pagination
    def get_queryset(self):
        filter_val = self.request.GET.get("filter", "")
        order_by = self.request.GET.get("orderby", "pk")
        if filter_val != "":
            tag = Tag.objects.filter(Q(title__contains=filter_val) | Q(
                description__contains=filter_val)).order_by(order_by)
        else:
            tag = Tag.objects.all().order_by(order_by)

        return tag

    def get_context_data(self, **kwargs):
        context = super(TagListView, self).get_context_data(**kwargs)
        context["filter"] = self.request.GET.get("filter", "")
        context["orderby"] = self.request.GET.get("orderby", "pk")
        context["segment"] = "برچسب ها"
        context["all_table_fields"] = Tag._meta.get_fields()
        return context


class CreateTagView(SuccessMessageMixin, PermissionRequiredMixin ,LoginRequiredMixin, CreateView):
    permission_required = "tag.create_tag"
    model = Tag
    template_name = 'dashboard/tag/create.html'
    form_class = TagForm
    title = 'create'
    success_url = reverse_lazy('tag:tag-list')
    success_message = "پست شما با موفقیت ایجاد شد"

    def handle_no_permission(self):
        messages.warning(self.request, "شما اجازه دسترسی به این صفحه رو ندارید")
        return redirect("dashboard:home")


class DeleteTagView(SuccessMessageMixin, PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Tag
    permission_required = "tag.delete_tag"
    template_name = 'dashboard/tag/list.html'
    success_url = reverse_lazy('tag:tag-list')
    success_message = "پست با موفقیت حذف گردید"


    def handle_no_permission(self):
        messages.warning(self.request, "شما اجازه دسترسی به این صفحه رو ندارید")
        return redirect("dashboard:home")

    def get(self, request, *args, **kwargs):
        slug=kwargs.get("slug")
        if slug is not None:
            tag_object = Tag.objects.get_queryset().filter(slug= slug)
            if tag_object is not None:
                tag_object.delete()
                messages.success(request, 'برچسب شمابا موفقیت حذف گردید') 
                return redirect('tag:tag-list')
        return redirect('dashboard/tag/list.html')
       


class TagUpdateView(SuccessMessageMixin,PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Tag
    permission_required = "tag.update_tag"
    template_name = 'dashboard/tag/edit.html'
    fields = "__all__" 
    success_url = reverse_lazy('tag:tag-list')

    def handle_no_permission(self):
        messages.warning(self.request, "شما اجازه دسترسی به این صفحه رو ندارید")
        return redirect("dashboard:home")

