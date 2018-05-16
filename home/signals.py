from typing import Optional

from django.conf import settings
from django.contrib.auth.models import Group, User
from django.db.models.signals import post_save
from django.dispatch import receiver

from stats.models import GuildMembership, RoleMembership


@receiver(post_save, sender=User)
def user_post_save(
    sender: type,
    instance: User,
    created: bool,
    raw: bool,
    using: str,
    update_fields: Optional[set],
    **kwargs
):
    """Add the appropriate authentication groups to the user.

    Args:
        sender (django.contrib.auth.models.User):
            The model class.
        instance (django.contrib.auth.models.User):
            The actual instance being saved.
        created (bool):
            `True` if a new record was created,
            `False` if it was just updated.
        raw (bool):
            `True` if the model is saved exactly as presented.
        using (str):
            The database alias being used.
        update_field (Optional[set]):
            The set of fields to update as passed to `User.save`,
            or `None` if none were passed.
        kwargs:
            Required by django to pass further arguments.

    Notes:
        See https://docs.djangoproject.com/en/2.0/ref/signals/#django.db.models.signals.post_save
        for further details on the `post_save` signal.
    """

    if created and instance.username != settings.ANONYMOUS_USER_NAME:
        # Is the newly created user a staff member on the Discord server?
        is_staff = RoleMembership.objects.filter(
            user_id=instance.id,
            guild_id=settings.DISCORD_GUILD_ID,
            role_id=settings.DISCORD_ADMIN_ROLE_ID,
        ).exists()

        if is_staff:
            # If so, fetch the `staff` group and add it to the user's groups
            staff_group = Group.objects.get(name='staff')
            instance.groups.add(staff_group)

        else:
            # Is the newly created user a member of the Discord server?
            is_member = GuildMembership.objects.filter(
                user_id=instance.id, guild_id=settings.DISCORD_GUILD_ID, is_member=True
            ).exists()

            if is_member:
                # If so, fetch the `member` group and add it to the user's groups
                member_group = Group.objects.get(name='member')
                instance.groups.add(member_group)

            else:
                # Otherwise, give the user the default `guest` group
                guest_group = Group.objects.get(name='guest')
                instance.groups.add(guest_group)
