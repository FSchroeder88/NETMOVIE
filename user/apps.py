from django.apps import AppConfig

class ProfilesConfig(AppConfig):
    # default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'

    def ready(self):
        import user.signals


