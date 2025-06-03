from django.apps import AppConfig


class MessengerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'messenger'

    def ready(self):
        from .services.bloomfilter import BloomFilterService

        BloomFilterService()

