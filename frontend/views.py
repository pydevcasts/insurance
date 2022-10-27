from django.shortcuts import get_object_or_404, render
from blog.forms import CommentForm
from blog.models import Comment, Post
from category.models import SubCategory
from django import template
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib import messages
from news.models import New
from newsletters.forms import NewsLettersForm
from django.shortcuts import redirect, render
from django.views.generic.detail import DetailView
from newsletters.models import NewsLetter, decrypt_email
from django.views.generic.edit import FormMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



def post_subcategory_list(request, slug=None):
    posts = Post.objects.published().select_related('subcategory').order_by('subcategory__category_id').distinct('subcategory__category')
    news = New.objects.filter(status = 1).order_by('-published_at')
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
                                                        'news':news
                                                        })

def all_post_view(request):
    title = "همه پست ها"
    all_post = Post.objects.all().filter(status= 1).select_related('subcategory').order_by('subcategory__category_id').distinct('subcategory__category')
    page = request.GET.get('page', 1)

    paginator = Paginator(all_post, 15)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request, "frontend/posts/index.html", {"all_post":all_post, "title":title, 'page_obj': page_obj})



class PostDetailView(FormMixin, DetailView):
    template_name = 'frontend/landing/detail.html'
    model = Post
    slug_field = 'slug'
    form_class = CommentForm
    obj = None
    list_ip = []
    def get_initial(self):
        instance = self.get_object()
       
        return {
            'content_type':instance.get_content_type,
            'object_id':instance.uid
        }
    
    def get_success_url(self):
        return reverse("detail", kwargs={"slug": self.object.slug})
  
    

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        post = get_object_or_404(Post, slug = self.kwargs['slug'])
        comments = Comment.objects.filter_by_instance(post)
        context['comments'] = comments
        context['title'] = "جزییات"
        context['form'] = self.get_form_class()
   
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        self.list_ip.append(ip)
        if ip in self.list_ip:
            post.view = ""
        else:
            post.views += 1
            post.save()
        return context


    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            self.object = self.get_object()
            form = self.get_form_class()
            form = CommentForm(instance=self.obj, data=request.POST)

            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
       

    def form_valid(self, form):
        if not self.request.user.is_authenticated:
                messages.info(self.request,"برای ارسال پیام نیازبه ثبت نام دارید !")
                return HttpResponseRedirect("/signup/")

        user = self.request.user
        comment_content = form.cleaned_data['content']
        reply_id = self.request.POST.get('comment_id') #reply-section
        comment_qs = None
        
        if reply_id:
            comment_qs = Comment.objects.get(id = reply_id)
            Comment.objects.create(
                content_object=comment_qs,
                content=comment_content,
                user=user,
            )
    
            messages.success(self.request, "پیامتان با موفقیت ارسال شد!")
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

        Comment.objects.create(
                content_object=Post.objects.get(slug=self.kwargs.get("slug")),
                content=comment_content,
                user=user,
                
            )
        messages.success(self.request, "پیامتان با موفقیت ارسال شد!")
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
        

    def form_invalid(self, form) -> HttpResponse:
        messages.error(self.request, "پیامتان با مشکل مواجه شد!")
        return super().form_invalid(form)





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


