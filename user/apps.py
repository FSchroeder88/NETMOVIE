from django.apps import AppConfig

class ProfilesConfig(AppConfig):
    name = 'user'

    def ready(self):
        import user.signals


