
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from faq.forms import FaqForm
from faq.models import Answer, Question

@method_decorator(csrf_exempt, name='dispatch')
class CreateFAQView(SuccessMessageMixin, CreateView):

    form_class = FaqForm
    template_name: 'frontend/faq/index.html'

    def post(self,request, *args, **kwargs):
        if request.method == "POST":
            form  = FaqForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "سوالتان با موفقیت ارسال گردید!!")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request, "پیام شما مشکل دارد")
        else:
            form = FaqForm()
        return render(request,'frontend/faq/index.html', {"form":form})



    def get(self, request, *args, **kwargs):
        questions = Question.objects.filter(status = 1)
        answer = Answer.objects.prefetch_related('question').first()
        context = {
            'questions':questions,
            'answer':answer,
            'title':'FAQ'
        }
    
        return render(request,'frontend/faq/index.html', context)

    


