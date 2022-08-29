
from newsletters.forms import NewsLettersForm
from newsletters.models import NewsLetter
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import  render

class NewsLetterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request):
        if request.method == 'POST':
            form_news = NewsLetter(subscriber=request.POST['subscriber'])
            if NewsLetter.objects.filter(subscriber=form_news.subscriber).exists():
                messages.error(request,"این ایمیل قبلا ثبت شده است")
            else:
                form_news.save()
                messages.success(request,
                                    "اشتراک شمابا موفقیت ثبت گردید !")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
         
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'),
                        {'form_news': NewsLettersForm() } 
                    )

        return self.get_response(request)