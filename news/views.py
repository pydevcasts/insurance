
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from news.models import New


class NewListView(ListView):

    def get(self, request, *args, **kwargs):
        news = New.objects.filter(status= 1).select_related('categories').order_by('-published_at')
        page = request.GET.get('page', 1)
        paginator = Paginator(news, 15)
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
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
    return render(request,
                'frontend/news/detail.html',
                {'new': new, 'title':'جزییات خبر' , 'favorites':favorites})


        