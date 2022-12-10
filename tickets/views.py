from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from . models import Ticket, Attachment, FollowUp
from django.shortcuts import redirect, render
from . forms import TicketCreateForm, FollowupForm, AttachmentFormSet
from django.contrib import messages
from django.core.mail import send_mail
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query_utils import Q
from contact.tasks import my_first_task



class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    context_object_name = 'tickets'
    template_name = 'dashboard/ticket/list.html'
    paginate_by = 20
   

    def get_queryset(self):
        filter_val = self.request.GET.get("filter", "")
        order_by = self.request.GET.get("orderby", "pk")
        if filter_val != "":
            ticket = Ticket.objects.filter(Q(title__contains=filter_val) | Q(
                description__contains=filter_val)).order_by(order_by).filter(user = self.request.user)
        else:
            ticket = Ticket.objects.all().order_by(order_by).filter(user = self.request.user)
        return ticket
        
      
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = self.request.GET.get("filter", "")
        context["orderby"] = self.request.GET.get("orderby", "pk")
        context["all_table_fields"] = Ticket._meta.get_fields()
        context['segment'] = 'لیست تیکت'
        return context




class AttachmentInline():
    form_class = TicketCreateForm
    model = Ticket
    template_name = "dashboard/ticket/ticket_create.html"

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))
        self.object = form.save()

        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('tickets:ticket-list')



    def formset_attachments_valid(self, formset):
        attachmets = formset.save(commit=False)  
        for obj in formset.deleted_objects:
            obj.delete()
        for attachmet in attachmets:
            attachmet.ticket = self.object
            attachmet.save()



class TicketCreate(AttachmentInline, LoginRequiredMixin, CreateView):

    def post(self, request, *args, **kwargs):
            if request.method == 'POST':
                form = TicketCreateForm(request.POST)
                if form.is_valid():
                    form = form.save(commit=False)
                    form.user = request.user
                    form.status = "TODO"
                    form.save()
                    my_first_task.delay(15)
                # mail notification of user to academybime
                    notification_subject = "[#" + str(form.user.id) + "] آکادمی بیمه"
                    notification_body = "سلام,\n\n یک تیکت  ارسال کردید    #" + "\n\nممنون از همراهی شما"
                    send_mail(notification_subject, notification_body, 'siyamak1981@gmail.com',
                        [form.user.email, 'siyamak1981@gmail.com'], fail_silently=False)
                    messages.success(request,
                                    "پیام شما با موفقیت ارسال گردید !")
                    return redirect('tickets:ticket-list')
            else:
                form = TicketCreateForm()
            return render(request, 'dashboard/ticket/ticket_create.html',
                        {'form': form , "segment":"ایجاد تیکت"} 
                    )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx


    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'attachments': AttachmentFormSet(prefix='attachments'),
            }
        else:
            return {
                'attachments': AttachmentFormSet(self.request.POST or None, self.request.FILES or None, prefix='attachments'),
            }



   
class TicketUpdate(AttachmentInline, LoginRequiredMixin, UpdateView):
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        return {
            'attachments': AttachmentFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='attachments'),
        }
    


def delete_attachments(request, pk):
    attachment =get_object_or_404(Attachment, pk = pk)
    attachment.delete()
    messages.success(
            request, 'فیل با موفقیت حذف گردید!'
            )
    return redirect('tickets:update_ticket', pk=attachment.ticket.id)



@login_required
def ticket_detail_view(request, pk):
    ticket = get_object_or_404(Ticket, pk= pk)
    attachments = Attachment.objects.filter(ticket = ticket)
    followups = FollowUp.objects.filter(ticket = ticket)
   
    return render(request, 'dashboard/ticket/ticket_detail.html', 
                {'ticket': ticket,
                   'attachments': attachments,
                   'followups': followups, 
                   'segment':'جزییات تیکت'})



class  FollowupReplyView(LoginRequiredMixin, CreateView):
    form_class =FollowupForm
    template_name='dashboard/ticket/followup_reply.html'

    def post(self, request, *args, **kwargs):
        follow = FollowUp.objects.get(id=self.kwargs['pk'])
      
        if request.method == "POST":
            form = FollowupForm(request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.user = request.user
                form.ticket = follow.ticket
                form.save()
                my_first_task.delay(2)
                # mail notification of user to academybime
                notification_subject = "[#" + str(follow.id) + "] آکادمی بیمه"
                notification_body = "سلام,\n\n یک تیکت جدید ارسال کردید  #" + "\n\nممنون از همراهی شما"
                send_mail(notification_subject, notification_body, 'siyamak1981@gmail.com',
                        [follow.ticket.user.email,follow.user.email], fail_silently=False)
                return redirect('tickets:ticket_detail',pk=follow.ticket.id)





