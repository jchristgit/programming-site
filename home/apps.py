from django.apps import AppConfig


class HomeConfig(AppConfig):
    name = "home"

    def ready(self):
        """Hook the `user_post_save` signal into Django."""

        from . import signals  # noqa
