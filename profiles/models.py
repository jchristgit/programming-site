from markupfield.fields import MarkupField
from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = MarkupField(
        max_length=500,
        blank=True,
        help_text="A short bio about you, shown on your profile."
    )
