from django.apps import AppConfig


class DjangoApp01Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_app01'

    def ready(self):
        import django_app01.signals