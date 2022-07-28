from django.db import models
from .querysets import PostStatusQuerySet

class PostPublishedManager(models.Manager):
    def get_queryset(self):
        return PostStatusQuerySet(self.model, using=self._db)

    def drafts(self):
        return self.get_queryset().drafts()
    
    def published(self):
        return self.get_queryset().published()

