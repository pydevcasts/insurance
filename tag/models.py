from django.utils.translation import gettext as _

from painless.models.mixins import OrganizedMixin


class Tag(OrganizedMixin):
    class Meta:
        ordering = [ '-title' ]
        verbose_name = _('برچسب')
        verbose_name_plural = _('برچسبها')
     
    
    def __str__(self):
        return self.title
 

