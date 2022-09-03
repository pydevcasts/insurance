

from django.http import HttpResponseRedirect,HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import  redirect
from django.utils.deprecation import MiddlewareMixin
User = get_user_model()

from renewal.forms import RenewalForm

class RenewalMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    # def process_request(self, request):
    #     if not request.user.is_authenticated():
    #             messages.info(request,"قبل از هر چیز ثبت نام کنید لطفا!")
    #             return HttpResponseRedirect("/signup/")


    def __call__(self, request):
        if request.method == "POST":
            form = RenewalForm(request.POST)
           
  
            if form.is_valid():
                form.save()
                messages.success(request,"اطلاعات شما با موفقیت ثبت گردید!")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request,"اطلاعات شما  اشتباه ثبت گردید!")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
        else:
            form = RenewalForm()
           

        return self.get_response(request)