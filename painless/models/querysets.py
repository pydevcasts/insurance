from django.db import models

class PostStatusQuerySet(models.QuerySet):
    def drafts(self):
        return self.filter(status = 0)

    def published(self):
        return self.filter(status = 1)
