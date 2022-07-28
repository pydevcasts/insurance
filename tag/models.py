from painless.models.mixins import OrganizedMixin
from django.utils.translation import gettext as _


class Tag(OrganizedMixin):
    class Meta:
        ordering = [ '-created' ]
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
     
    
    def __str__(self):
        return self.title
 

