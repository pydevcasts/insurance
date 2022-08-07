from django.apps import AppConfig


class TagConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tag'
    verbose_name = "بر چسب ها"
    
    
    def ready(self):
        import tag.signals