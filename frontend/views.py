from django.shortcuts import get_object_or_404, render
from blog.models import Post
from category.models import Category,SubCategory
from django import template
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib import messages
from newsletters.forms import NewsLettersForm
from django.shortcuts import redirect, render

from newsletters.models import NewsLetter, decrypt_email

def post_subcategory_list(request, slug=None):
    category = None
    categories = Category.objects.all()
    posts = Post.objects.all()
    postlists = Post.objects.filter(status = "1")
 
    if slug:
        subcategory = get_object_or_404(SubCategory, slug=slug)
        posts = posts.filter(subcategory=subcategory)
    if request.method == 'POST':
        form = NewsLettersForm(request.POST or None)
        if form.is_valid():
            form = form.save(commit=False)
            
            if NewsLetter.objects.filter(email=form.email).exists():
                messages.error(request,"این ایمیل قبلا ثبت شده است")
                messages.error(request, form.errors)
                print("این ایمیل قبلا ثبت شده است")
            else:
                form.save()
                messages.success(request,
                                "اشتراک شمابا موفقیت ثبت گردید !")
                return redirect("frontend:post_and_subcategory")
    else:
        form = NewsLettersForm()
    return render(request, "frontend/landing/home.html", {
                                                        "categories": categories,
                                                        "posts": posts,
                                                        "category": category,
                                                        "postlists":postlists,
                                                        "form":form
                                                        })

def unsubscrib_redirect_view(request, token, *args, **kwargs):
        print("token:", token)
        email = decrypt_email(token)
        print("email:", email)
        try :
            email_obj = NewsLetter.objects.get(email = email)
            email_obj.delete()
            messages.success(request,"شما با موفقیت اشتراک خود را حذف نمودید")
        except NewsLetter.DoesNotExist:
            print(
                 "ایمیل وجود ندارد"
            )
            html_template = loader.get_template('backend/dashboard/page-403.html')
            return HttpResponse(html_template.render({"title":" شما قبلا اشتراک خود را لغو نمودید"}, request))

        return redirect("frontend:post_and_subcategory")


def pages(request):
    context = {}
    try:
        load_template = request.path.split('/')[-1]

        if load_template == 'frontend':
            return HttpResponseRedirect(reverse('dashboard:post_and_subcategory'))
        context['segment'] = load_template

        html_template = loader.get_template('dashboard/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('backend/dashboard/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('backend/dashboard/page-500.html')
        return HttpResponse(html_template.render(context, request))


