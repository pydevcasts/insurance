
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.shortcuts import redirect
from django.urls.base import  reverse_lazy
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, DeleteView, FormView,UpdateView
from tag.models import Tag
from tag.forms import GenerateRandomTagForm, TagForm
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from tag.tasks import create_random_tag


# @method_decorator(cache_page(60 * 60 * 24), name='dispatch')
class TagListView(LoginRequiredMixin, ListView):
    model = Tag
    context_object_name = 'tags'
    template_name = 'backend/tag/list.html'
    paginate_by = 10

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
        context["all_table_fields"] = Tag._meta.get_fields()
        return context


class CreateTagView(SuccessMessageMixin, PermissionRequiredMixin ,LoginRequiredMixin, CreateView):
    permission_required = "tag.create_tag"
    model = Tag
    template_name = 'backend/tag/create.html'
    form_class = TagForm
    title = 'create'
    success_url = reverse_lazy('tag:list')
    success_message = "Tag Create successfully"

    def handle_no_permission(self):
        messages.warning(self.request, "You dont have permission to this page please signin with superuser!")
        return redirect("dashboard:home")

class DeleteTagView(SuccessMessageMixin, PermissionRequiredMixin, DeleteView):
    model = Tag
    permission_required = "tag.delete_tag"
    template_name = 'backend/tag/list.html'
    success_url = reverse_lazy('tag:list')
    success_message = "Tag Delete successfully"


    def handle_no_permission(self):
        messages.warning(self.request, "You dont have permission to this page please signin with superuser!")
        return redirect("dashboard:home")

    def get(self, request, *args, **kwargs):
        slug=kwargs.get("slug")
        if slug is not None:
            tag_object = Tag.objects.get_queryset().filter(slug= slug)
            if tag_object is not None:
                tag_object.delete()
                messages.success(request, 'Your profile was updated.') 
                return redirect('tag:list')
        return redirect('backend/tag/list.html')
       


class TagUpdateView(SuccessMessageMixin,UpdateView):
    model = Tag
    template_name = 'backend/tag/edit.html'
    fields = "__all__" 
    success_url = reverse_lazy('tag:list')

    def handle_no_permission(self):
        messages.warning(self.request, "You dont have permission to this page please signin with superuser!")
        return redirect("dashboard:home")


class GenerateRandomTagView(FormView):
    template_name = 'backend/user/generate_random_users.html'
    form_class = GenerateRandomTagForm

    def form_valid(self, form):
        total = form.cleaned_data.get('total')
        create_random_tag.delay(total)
        messages.success(self.request, 'We are generating your random tags! Wait a moment and refresh this page.')
        return redirect('tag:list')