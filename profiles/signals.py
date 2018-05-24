from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import RestrictProcessing


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    """Called when a User is created or updated.

    Adds a `RestrictProcessing` entry for the given user.
    """

    if created:
        RestrictProcessing.objects.create(user=instance)
