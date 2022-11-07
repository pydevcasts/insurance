from django.db import models
from .querysets import NewQuerySet, PostStatusQuerySet



class PostPublishedManager(models.Manager):
    def get_queryset(self):
        return PostStatusQuerySet(self.model, using=self._db)

    def drafts(self):
        return self.get_queryset().drafts()
    
    def published(self):
        return self.get_queryset().published()



class NewManager(models.Manager):
    def get_queryset(self):
        return NewQuerySet(self.model, using=self._db)

    def most_views_by_users(self):
        return self.get_queryset().total_view()
    
    