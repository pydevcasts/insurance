from django.shortcuts import render
from search.documents import PostDocument
from elasticsearch_dsl import Q

def search_post(request):
    q = request.GET.get("q")
    if q:
        posts = PostDocument.search().query((Q("multi_match", query=q, fields=['title', 'summary'])))
        posts = posts.exclude('match', draft=True)
        

    else:
        posts = ""
       
    return render (request, "frontend/search/search.html", {"posts":posts})

