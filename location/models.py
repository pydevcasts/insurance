from django.db import models


class Location(models.Model):
    address = models.CharField(max_length=200, null = True)
    date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.address