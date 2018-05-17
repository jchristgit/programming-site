from django.apps import AppConfig


class GuidesConfig(AppConfig):
    name = "guides"

    def ready(self):
        """Hook the Guide post save signal into Django."""

        from . import signals  # noqa
