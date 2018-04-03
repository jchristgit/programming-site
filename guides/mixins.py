from django.conf import settings
from django.http import HttpResponseForbidden

from stats.models import (
    GuildMembership,
    RoleMembership,
    Users as DiscordUser
)


class MemberRequiredMixin:
    """
    Checks that the user associated with the request
    is a member of the guild specified as `DISCORD_GUILD_ID`
    in the settings. If not, returns Forbidden.
    """

    def dispatch(self, request, *args, **kwargs):
        is_member = GuildMembership.objects.using('stats').filter(
            user_id=request.user.id,
            guild_id=settings.DISCORD_GUILD_ID,
            is_member=True
        ).exists()
        if not is_member:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)


class AuthorRequiredMixin:
    """
    Checks that the user associated with the request
    is the author of the object captured within it,
    or alternatively is an admin - this is checked
    by testing their role membership against `DISCORD_ADMIN_ROLE_ID`
    from the settings. If these fail, returns Forbidden.
    """

    def dispatch(self, request, *args, **kwargs):
        is_author = self.request.user == self.object.author
        is_admin = RoleMembership.objects.using('stats').filter(
            user_id=request.user.id,
            guild_id=settings.DISCORD_GUILD_ID,
            role_id=settings.DISCORD_ADMIN_ROLE_ID
        ).exists()
        if not (is_author or is_admin):
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)


class AddRequestDiscordUserMixin:
    """
    Adds `discord_user` to a template which is
    constructed from the user id of `request.user`.
    If the logged in user is anonymous, this is `None`.
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['discord_user'] = DiscordUser.from_django_user(self.request.user)
        return context


class AddIsMemberContextMixin:
    """
    Adds `is_member` to the template context which
    specifies whether the request user is a member
    of the guild specified as `DISCORD_GUILD_ID`.
    """

    def get_context_data(self, **kwargs):
        print("I'm getting called!")
        context = super().get_context_data(**kwargs)
        context['is_member'] = GuildMembership.objects.using('stats').filter(
            user_id=self.request.user.id,
            guild_id=settings.DISCORD_GUILD_ID,
            is_member=True
        ).exists()
        return context


class AddIsAdminContextMixin:
    """
    Adds `is_admin` to the template context which
    specifies whether the request user is an administrator
    of the guild specified as `DISCORD_GUILD_ID` in
    the setting by testing their role membership
    against `DISCORD_ADMIN_ROLE_ID`.
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin'] = RoleMembership.objects.using('stats').filter(
            user_id=self.request.user.id,
            guild_id=settings.DISCORD_GUILD_ID,
            role_id=settings.DISCORD_ADMIN_ROLE_ID
        ).exists()
        return context
