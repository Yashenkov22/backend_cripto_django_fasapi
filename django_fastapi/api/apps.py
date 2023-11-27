from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = "api"
    verbose_name = 'Безналичные'

    def ready(self) -> None:
        import api.signals
