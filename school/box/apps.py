from django.apps import AppConfig


class BoxConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'box'
    
    def ready(self):
        import box.signals
    
