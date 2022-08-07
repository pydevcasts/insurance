from newsletters.forms import NewsLettersForm
from django.contrib.auth import get_user_model

from newsletters.models import NewsLetters
User = get_user_model()



from django.core.cache import cache
from django.db import connections, transaction


class NewsLettersMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)
        


    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.method == "POST" :
        
        
            form = NewsLettersForm(request.POST)

            if form.is_valid() :
                # NewsLetters.objects.filter(email = form.cleaned_data['email'])
                form.save()    

        # cache.clear()
        # cursor = connections['cache_database'].cursor()
        # cursor.execute('DELETE FROM my_cache_table')
        # transaction.commit_unless_managed(using='my_cache_table')
 
