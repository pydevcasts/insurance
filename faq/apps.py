from django.apps import AppConfig


class FaqConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'faq'
    verbose_name_plural = 'سوالها'

    
    def ready(self):
        import faq.signals