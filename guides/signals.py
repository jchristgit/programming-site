from django.db.models.signals import post_save
from django.dispatch import receiver
from guardian.shortcuts import assign_perm

from .models import Guide


@receiver(post_save, sender=Guide)
def guide_post_save(sender, instance, created, **kwargs):
    """Called when a guide is saved.

    Gives the guide author the necessary permissions
    to change the guide and delete the guide.
    """

    if created:
        assign_perm('change_guide', instance.author, instance)
        assign_perm('delete_guide', instance.author, instance)
