from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from . models import Ticket, Attachment, FollowUp
from django.shortcuts import redirect, render
from  django.utils import timezone
from . forms import TicketCreateForm, TicketEditForm, FollowupForm, AttachmentForm
from django.contrib import messages
from contact.tasks import my_first_task
from django.core.mail import send_mail


@login_required
def all_tickets_view(request):
    if request.user.is_superuser:
        ticket_open = Ticket.objects.all().exclude(status__exact = "DONE")
        return render(request, 'backend/ticket/list.html', {'tickets':ticket_open})
    else:
        ticket_open = Ticket.objects.all().exclude(status__exact = "DONE").filter(owner = request.user)
        return render(request, 'backend/ticket/list.html', {'tickets':ticket_open})


@login_required
def my_tickets_view(request):
    tickets = Ticket.objects.filter(assigned_to=request.user).exclude(status__exact = "DONE")
    tickets_waiting = Ticket.objects.filter(status__exact= "WAITING").filter(waiting_for= request.user)
    return render(request, 'backend/ticket/my-tickets.html', {'tickets':tickets, 'tickets_waiting':tickets_waiting})


@login_required
def ticket_detail_view(request, pk):
    ticket = get_object_or_404(Ticket, pk= pk)
    attachments = Attachment.objects.filter(ticket = ticket)
    followups = FollowUp.objects.filter(ticket = ticket)
    return render(request, 'backend/ticket/ticket_detail.html', 
                {'ticket': ticket,
                   'attachments': attachments,
                   'followups': followups, })

@login_required
def ticket_create_view(request):
    if request.method == "POST":
        form = TicketCreateForm(request.POST)
        if form.is_valid():
            obj = form.save(commit = False)
            obj.owner = request.user
            obj.status = "TODO"
            obj.save()
            messages.success(request,
                                    "Tank you for contact us!")
            return redirect('tickets:my-tickets')
    else:
        form = TicketCreateForm()
    return render(request, 'backend/ticket/ticket_create.html', { 'form': form })

@login_required
def ticket_edit_view(request, pk):
    data = get_object_or_404(Ticket, pk= pk)
 
    if request.method == "POST":
        form = TicketEditForm(request.POST, instance = data)
        if form.is_valid():
            if form.cleaned_data['status'] == "DONE":
                data.close_date = timezone.now()
            form.save(commit=False)
            form.user = request.user
            form.modified = timezone.now()
            form.save()
 
            messages.success(request, "Your Ticket is Updated Successfully! ")
            return redirect('tickets:list')
    else:
        form = TicketEditForm(instance = data)
    return render(request, 'backend/ticket/ticket_edit.html', { 'form': form })



@login_required
def followup_create_view(request):
   
    if request.method == "POST":
        form = FollowupForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            ticket = Ticket.objects.get(id=request.POST['ticket'])
            # my_first_task.delay(2)
        
            # mail notification to owner of ticket
            notification_subject = "[#" + str(ticket.id) + "] New followup"
            notification_body = "Hi,\n\n new followup created for ticket #" \
                                + str(ticket.id) \
                                + " (http://localhost:8000/ticket/" \
                                + str(ticket.id) 
                              

            send_mail(notification_subject, notification_body, 'siyamak1981@gmail.com',
                      [ticket.owner.email], fail_silently=False)
            messages.success(request, "your comments is added successfully!")
            return redirect('tickets:followup_new')

    else:
        form = FollowupForm(initial={'ticket': request.GET.get('ticket'),
                                     'user': request.user})
    return render(request,
                  'backend/ticket/followup_edit.html',
                  {'form': form, })


def followup_edit_view(request, pk):

    data = get_object_or_404(FollowUp, pk = pk )

    if request.POST:
        form = FollowupForm(request.POST, instance=data)
        if form.is_valid():
            form.save()

            return redirect('tickets:list')

    else:
        form = FollowupForm(instance=data)

    return render(request,
                  'backend/ticket/followup_edit.html',
                  {'form': form, })




def attachment_create_view(request):

    if request.POST:
        form = AttachmentForm(request.POST, request.FILES)

        if form.is_valid():
            form.save(commit = False)
            form.user = request.user
            form.save()
            messages.success(request,
                                 "Attach added successfull!")
            return redirect('tickets:list')

    else:
        form = AttachmentForm(request.FILES)

    return render(request,
                  'backend/ticket/attachment_add.html',
                  {'form': form, })


