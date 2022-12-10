from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import New


class StaticViewSitemap(Sitemap):

    priority = 1.0
    changefreq = 'daily'
    def items(self):
        return ['new:list_news']

    def location(self, item):
            return reverse(item)

class NewSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7
    def items(self):
        return New.objects.all()

    def location(self, obj):
        pass

    def lastmod(self, obj): 
        return obj.published_at