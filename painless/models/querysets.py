from django.db import models
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta



class PostStatusQuerySet(models.QuerySet):
    def drafts(self):
        return self.filter(status = 0)

    def published(self):
        return self.filter(status = 1,published_at__lte= timezone.now() )


class NewQuerySet(models.QuerySet):
    def total_view(self):
        return self.annotate(total_views=Count('views')).filter(published_at__gte=timezone.now() - timedelta(days=100),\
            total_views__gt=0, status = 1).order_by('-views')

