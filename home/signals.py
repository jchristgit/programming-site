from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from stats.models import GuildMembership, RoleMembership


@receiver(post_save, sender=SocialAccount)
def social_account_post_save(sender, instance, **kwargs):
    """Add the appropriate authentication groups to the user.

    Notes:
        See http://django-allauth.readthedocs.io/en/latest/signals.html#allauth-socialaccount.
    """

    user = instance.user

    if user.username != settings.ANONYMOUS_USER_NAME:
        # Delete any existing groups
        user.groups.clear()

        # Is the newly created user a staff member on the Discord server?
        is_staff = RoleMembership.objects.filter(
            user_id=instance.uid,
            guild_id=settings.DISCORD_GUILD_ID,
            role_id=settings.DISCORD_ADMIN_ROLE_ID,
        ).exists()

        if is_staff:
            # If so, fetch the `staff` group and add it to the user's groups
            staff_group = Group.objects.get(name='staff')
            user.groups.add(staff_group)

        else:
            # Is the newly created user a member of the Discord server?
            is_member = GuildMembership.objects.filter(
                user_id=instance.uid,
                guild_id=settings.DISCORD_GUILD_ID,
                is_member=True
            ).exists()

            if is_member:
                # If so, fetch the `member` group and add it to the user's groups
                member_group = Group.objects.get(name='member')
                user.groups.add(member_group)

            else:
                # Otherwise, give the user the default `guest` group
                guest_group = Group.objects.get(name='guest')
                user.groups.add(guest_group)
