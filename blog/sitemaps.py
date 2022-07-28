from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from blog.models import Post


class StaticViewSitemap(Sitemap):

    priority = 1.0
    changefreq = 'daily'
    def items(self):
        return ['blog:list']

    def location(self, item):
            return reverse(item)

class PostSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7
    def items(self):
        return Post.objects.all()

    def location(self, obj):
        pass

    def lastmod(self, obj): 
        return obj.published_at