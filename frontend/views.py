from django.shortcuts import get_object_or_404, render
from blog.models import Post
from category.models import SubCategory
from django import template
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib import messages
from newsletters.forms import NewsLettersForm
from django.shortcuts import redirect, render
from django.views.generic.detail import DetailView
from newsletters.models import NewsLetter, decrypt_email
from tag.models import Tag



def post_subcategory_list(request, slug=None):
    posts = Post.objects.filter(status = "1").select_related('subcategory').order_by('subcategory__category_id').distinct('subcategory__category')
    postlists = posts[:5]
 
    if slug:
        subcategory = get_object_or_404(SubCategory, slug=slug)
        posts = posts.filter(subcategory=subcategory)
        
    if request.method == 'POST':
            form = NewsLetter(subscriber=request.POST['subscriber'])
            if NewsLetter.objects.filter(subscriber=form.subscriber).exists():
                messages.error(request,"این ایمیل قبلا ثبت شده است")
            else:
                form.save()
                messages.success(request,
                                    "اشتراک شمابا موفقیت ثبت گردید !")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
         
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'),
                        {'form': NewsLettersForm() } 
                    )

    return render(request, "frontend/landing/home.html", {
                                                        "posts": posts,
                                                        "postlists":postlists,
                                                        })



class PostDetailView(DetailView):
    template_name = 'frontend/landing/detail.html'
    model = Post

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["post"] = Post.objects.get(slug=self.kwargs.get("slug"))
        context["title"] = Post.objects.get(slug=self.kwargs.get("slug"))
        return context



def unsubscrib_redirect_view(request, token, *args, **kwargs):
        print("token:", token)
        email = decrypt_email(token)
  
        try :
            email_obj = NewsLetter.objects.get(subscriber = email)
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


