from django.apps import AppConfig


class UsertimelineConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usertimeline'

    def ready(self) -> None:
        from usertimeline import signals
