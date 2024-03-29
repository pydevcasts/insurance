from django.apps import AppConfig


class RenewalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'renewal'
    verbose_name = "تمدید ها"


    def ready(self):
        import renewal.signals