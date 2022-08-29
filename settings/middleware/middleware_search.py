from django.shortcuts import render
from search.documents import PostDocument
from elasticsearch_dsl import Q

class SearchMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request):
        if request.method == 'POST':
            q = request.GET.get("q")
            if q:
                searchs = PostDocument.search().query((Q("multi_match", query=q, fields=['title', 'summary'])))
                searchs = searchs.exclude('match', draft=True)
                print("lkdfjlkbd", searchs)
            else:
                searchs = ""
            
            return render (request, "frontend/search/search.html", {"searchs":searchs})

        return self.get_response(request)