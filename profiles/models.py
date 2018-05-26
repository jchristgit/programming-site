from django.conf import settings
from django.db import models


class RestrictProcessing(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True
    )
    restrict_processing = models.BooleanField(
        default=False,
        help_text="Make your profile invisible to other users."
    )
