from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver


ADMIN_PERMISSION_BITFLAGS = 0x8


@receiver(post_save, sender=SocialAccount)
def social_account_post_save(sender, instance, **kwargs):
    """Add the appropriate permission groups to the user.

    Uses data returned by Discord's OAuth to add the
    appropriate permission groups - for example, Guest,
    Member, or Staff - depending on their guild permissions.

    Notes:
        See http://django-allauth.readthedocs.io/en/latest/signals.html#allauth-socialaccount.
    """

    user = instance.user

    if user.username != settings.ANONYMOUS_USER_NAME:
        # Delete any existing groups
        user.groups.clear()

        guilds = instance.extra_data['guilds']
        guild_membership = next(
            (guild for guild in guilds if guild['id'] == str(settings.DISCORD_GUILD_ID)),
            None
        )

        # Is the newly created user a member of the Discord server?
        if guild_membership is None:
            # If not, give the user the default `guest` group
            guest_group = Group.objects.get(name='guest')
            user.groups.add(guest_group)

        # Does the newly created user have administrator permissions?
        elif bool(guild_membership['permissions'] & ADMIN_PERMISSION_BITFLAGS):
            # If so, fetch the `staff` group and add it to the user's groups
            staff_group = Group.objects.get(name='staff')
            user.groups.add(staff_group)

        # Otherwise, the user is a regular member of the server.
        else:
            member_group = Group.objects.get(name='member')
            user.groups.add(member_group)
