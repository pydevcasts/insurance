from django.shortcuts import get_object_or_404, render
from blog.models import Post
from category.models import Category,SubCategory
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views.generic import ListView


def post_subcategory_list(request, slug=None):
    category = None
    categories = Category.objects.all()
    posts = Post.objects.all()
    postlists = Post.objects.filter(status = "1")
 
    if slug:
        subcategory = get_object_or_404(SubCategory, slug=slug)
        posts = posts.filter(subcategory=subcategory)
    return render(request, "frontend/landing/home.html", {
                                                        "categories": categories,
                                                        "posts": posts,
                                                        "category": category,
                                                        "postlists":postlists
                                                        })



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


