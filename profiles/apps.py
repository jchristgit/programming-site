from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    name = "profiles"

    def ready(self):
        """Hook our User post save signal into Django."""

        from . import signals  # noqa
