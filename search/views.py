from django.shortcuts import render


def search_post(request):
    return render (request, "frontend/search/search.html")

