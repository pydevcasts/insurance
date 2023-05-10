

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from blog.models import Comment, Post
from category.models import Category
from comment.forms import CommentForm
from news.models import New
from newsletters.forms import NewsLettersForm
from newsletters.models import NewsLetter, decrypt_email


@csrf_exempt
def post_category_list(request, slug=None):
    posts = Post.objects.published().select_related('category').order_by('category_id').distinct('category')[:6]
    news = New.objects.filter(status = 1).order_by('-published_at')
 
    if slug:
        category = get_object_or_404(Category, slug=slug)
        posts = posts.filter(category=category)
        
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
                                                        'news':news,
                                                        'room_name': "broadcast" 
                                                        })


@csrf_exempt                                                     
def all_post_view(request):
    title = "همه پست ها"
    all_post = Post.objects.all().filter(status= 1).select_related('category').order_by('category_id').distinct('category')
    page = request.GET.get('page', 1)

    paginator = Paginator(all_post, 15)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request, "frontend/posts/index.html", {"all_post":all_post, "title":title, 'page_obj': page_obj})


@method_decorator(csrf_exempt, name='dispatch')
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
        return reverse("frontend:detail", args=[self.published_at.year,
                             self.published_at.month,
                             self.published_at.day, 
                             self.slug])
  

    def get(self, request,year, month,day,slug):
        post = get_object_or_404(Post, 
                                published_at__year=year,
                                published_at__month=month,
                                published_at__day=day,
                                slug=slug
                                )
        post.increase_view_count() # Increase view count
        return render(request, self.template_name, {"post": post})


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        post = get_object_or_404(Post, slug = self.kwargs['slug'])
       
        context['comments'] = Comment.objects.filter_by_instance(post)
        context['title'] = post.title
        context['segment'] = post.title
        context['form'] = self.get_form_class()
        context['favorites'] = New.objects.most_views_by_users()[:5]
        return context


    @csrf_exempt
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




@csrf_exempt
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
            html_template = loader.get_template('dashboard/dashboard/page-403.html')
            return HttpResponse(html_template.render({"title":" شما قبلا اشتراک خود را لغو نمودید"}, request))

        return redirect("blog:post_and_category")



def notification_broadcast(request):
    channel_layer = get_channel_layer()
    message = request.GET.get("message")
    # broadcast_notification.delay(),
    async_to_sync(channel_layer.group_send)(
        "notification_broadcast",
        

        {
            'type': 'send_notification',
             'notification':
        {
      
            'message': message
        }
        }
    ),
    return HttpResponse("Done")