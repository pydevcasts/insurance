
from django.http import  HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from renewal.forms import RenewalForm



class RenewalView(LoginRequiredMixin, CreateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request,"لطفا ثبت نام نمایید!")
            return redirect("accounts:signup")

        if request.method == 'POST':
            form = RenewalForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,"اطلاعات شما با موفقیت ثبت گردید!")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request,"اطلاعات شما اشتباه ثبت گردید!")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            form = RenewalForm()
        return render(request, 'frontend/includes/_renewal.html')


