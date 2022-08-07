from django.shortcuts import render
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.shortcuts import redirect, render
from faq.forms import FaqForm
from faq.models import FAQ, Answer, Question
from django.urls.base import reverse_lazy

class CreateFAQView(SuccessMessageMixin, CreateView):
    model = FAQ
    form_class = FaqForm
    template_name: 'frontend/faq/index.html'
    success_url = reverse_lazy('faq:faq-insurance')
    success_message = "سوالتان با موفقیت ارسال گردید!!"


    def get(self, request, *args, **kwargs):
        questions = Question.objects.filter(status = 1)
        answer = Answer.objects.prefetch_related('question').first()
        context = {
            'questions':questions,
            'answer':answer,
            'title':'FAQ'
        }
    
        return render(request,'frontend/faq/index.html', context)

    


