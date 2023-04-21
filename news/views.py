
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

from blog.models import Comment
from comment.forms import CommentForm
from news.models import New


class NewListView(ListView):

    def get(self, request, *args, **kwargs):
        news = New.objects.filter(status= 1).select_related('category').order_by('-published_at')
       
        page = request.GET.get('page', 1)
     
        paginator = Paginator(news, 15)
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        print(page_obj)
        return render(request, 'frontend/news/index.html', {'page_obj': page_obj,'title':'خبر ها','summary':'خبر های روز بیمه' })


def new_detail(request, year, month, day, slug):
    list_ip =[]
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    new = get_object_or_404(New,
                                status = 1,
                                published_at__year=year,
                                published_at__month=month,
                                published_at__day=day,slug=slug)
    list_ip.append(ip)
    if ip in list_ip:
        new.views += 0
    else:
        new.views += 1
    new.save()
    favorites = New.objects.most_views_by_users().exclude(slug = new.slug)[:5]
    comments = Comment.objects.filter_by_instance(new)
 
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            user = request.user
            comment_content = form.cleaned_data['content']
            reply_id = request.POST.get('comment_id') #reply-section
            comment_qs = None
            
            if reply_id:
                comment_qs = Comment.objects.get(id = reply_id)
                Comment.objects.create(
                    content_object=comment_qs,
                    content=comment_content,
                    user=user,
                )
        
                messages.success(request, "پیامتان با موفقیت ارسال شد!")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            Comment.objects.create(
                    content_object=New.objects.get(slug=slug),
                    content=comment_content,
                    user=user,
                    
                )
            messages.success(request, "پیامتان با موفقیت ارسال شد!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
       
    
    else:
        form = CommentForm()
    return render(request,
                'frontend/news/detail.html',
                {'new': new, 'title':new.title , 'segment':new.title, 'favorites':favorites, 'form':form ,'comments':comments})


