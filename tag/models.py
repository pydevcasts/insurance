from painless.models.mixins import OrganizedMixin
from django.utils.translation import gettext as _


class Tag(OrganizedMixin):
    class Meta:
        ordering = [ '-created' ]
        verbose_name = _('برچسب')
        verbose_name_plural = _('برچسبها')
     
    
    def __str__(self):
        return self.title
 

