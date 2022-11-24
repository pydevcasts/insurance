
from django.shortcuts import render
from django.views.generic import ListView
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .models import CustomerFeedback
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render



@method_decorator(cache_page(60 * 60 * 24), name='dispatch')
class CustomerFeedbackListView(ListView):

    def get(self, request, *args, **kwargs):
        customer_feedbacks = CustomerFeedback.objects.filter(status= 1).order_by('-published_at')
        page = request.GET.get('page', 1)
        paginator = Paginator(customer_feedbacks, 2)
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        return render (request, 'frontend/feedback/index.html', {
            'title':"بازخورد مشتریان",
            'customer_feedbacks':customer_feedbacks,
            'page_obj':page_obj
        })