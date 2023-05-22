import folium
import geocoder
from django.contrib import messages
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls.base import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from contact.forms import ContactForm
from contact.models import Contact, Location
from contact.tasks import my_first_task


class ListContactView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Contact
    permission_required = "contact.view_contact"
    context_object_name = 'contacts'
    template_name = 'dashboard/contact/list.html'
    paginate_by = 10

    def handle_no_permission(self):
        messages.warning(self.request, " شما اجازه دسترسی به این صفحه رو ندارید")
        return redirect("dashboard:home")


    def get_queryset(self):
        filter_val = self.request.GET.get("filter", "")
        order_by = self.request.GET.get("orderby", "pk")
        if filter_val != "":
            contact = Contact.objects.filter(Q(title__contains=filter_val) | Q(
                description__contains=filter_val)).order_by(order_by)
        else:
            contact = Contact.objects.all().order_by(order_by)

        return contact

    def get_context_data(self, **kwargs):
        context = super(ListContactView, self).get_context_data(**kwargs)
        context["filter"] = self.request.GET.get("filter", "")
        context["orderby"] = self.request.GET.get("orderby", "pk")
        context["all_table_fields"] = Contact._meta.get_fields()
        context["segment"] = "لیست تماس"
        return context
        

@method_decorator(csrf_exempt, name='dispatch')
class CreateContactView(SuccessMessageMixin , CreateView):
    def post(self, request, *args, **kwargs):
            if request.method == 'POST':
                form = ContactForm(request.POST)
                if form.is_valid():
                    form = form.save(commit=False)
                    my_first_task.delay(15)
                    form.save()
                    messages.success(request,
                                    "پیام شما با موفقیت ارسال گردید !")
                    return redirect("contact:contact-create")
            else:
                form = ContactForm()
            return render(request, 'frontend/contact/create.html',
                        {'form': form , "segment":"تماس با ما"} 
                    )


    def get(self, request, **kwargs):
        address = Location.objects.all().last()
        location = geocoder.osm(address)
        lat = location.lat
        lng = location.lng
        country = location.country
        map = folium.Map(location=[19,-12], zoom_start=2)
    
        folium.Marker([lat,lng],tooltip="click for more",popup = country).add_to(map)
        map = map._repr_html_()
        return render(request, 'frontend/contact/create.html',
                        {'map':map, 'segment': 'تماس با ما'}
                        )



@method_decorator(csrf_exempt, name='dispatch')
class DeleteContactView(SuccessMessageMixin, PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Contact
    permission_required = "contact.delete_contact"
    template_name = 'dashboard/contact/list.html'
    success_url = reverse_lazy('contact:list')
    success_message = "Contact Delete successfully"


    def handle_no_permission(self):
        messages.warning(self.request, " شما اجازه دسترسی به این صفحه رو ندارید")
        return redirect("dashboard:home")

    def get(self, request, *args, **kwargs):
        pk=kwargs.get("pk")
        if pk is not None:
            Contact_object = Contact.objects.get_queryset().filter(pk= pk)
            if Contact_object is not None:
                Contact_object.delete()
                messages.success(request, 'پست شما با موفقیت حذف گردید') 
                return redirect('contact:contact-list')
        return redirect('dashboard/Contact/list.html')
       


class ContactShowView(SuccessMessageMixin,PermissionRequiredMixin, LoginRequiredMixin,UpdateView):
    permission_required = "contact.update_contact"
    model = Contact
    template_name = 'dashboard/contact/show.html'
    fields = "__all__" 
    success_url = reverse_lazy('contact:contact-list')
    
    def handle_no_permission(self):
        messages.warning(self.request, " شما اجازه دسترسی به این صفحه رو ندارید")
        return redirect("dashboard:home")

