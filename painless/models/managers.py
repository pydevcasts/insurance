from django.db import models
from .querysets import NewQuerySet, PostStatusQuerySet
from django.contrib.contenttypes.models import ContentType



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
    
    


class CommentManager(models.Manager):
    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        object_id = instance.uid
        qs = super().filter(content_type=content_type, object_id=object_id)
        return qs