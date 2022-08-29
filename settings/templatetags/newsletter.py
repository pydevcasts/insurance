# from django.template import Library
# from django.contrib import messages
# from newsletters.forms import NewsLettersForm
# from django.shortcuts import redirect, render



# register = Library()

# @register.inclusion_tag('frontend/partials/_subscribe.html')
# def render_sample(request):
#     if request.method == 'POST' and prefix in request.POST:
        #     form = NewsLettersForm(request.POST or None)
        #     if form.is_valid():
        #         form = form.save(commit=False)
        #         if NewsLetter.objects.filter(subscriber=form.subscriber).exists():
        #             messages.error(request,"این ایمیل قبلا ثبت شده است")
        #             messages.error(request, form.errors)
    
        #         else:
        #             form.save()
        #             messages.success(request,
        #                             "اشتراک شمابا موفقیت ثبت گردید !")
        # else:
        #     form = NewsLettersForm()
#     return ({
                                                       
#                                                         "form_news":form_news
#                                                         })