from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from django.http import HttpResponseForbidden

from stats.models import GuildMembership, RoleMembership


class MemberRequiredMixin:
    """
    Checks that the user associated with the request
    is a member of the guild specified as `DISCORD_GUILD_ID`
    in the settings. If not, returns Forbidden.
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("You need to be logged in to do that.")

        try:
            social_account = SocialAccount.objects.get(user=request.user)
        except SocialAccount.DoesNotExist:
            return HttpResponseForbidden("You need to be logged in with Discord to do that.")

        is_member = GuildMembership.objects.filter(
            user_id=social_account.uid, guild_id=settings.DISCORD_GUILD_ID, is_member=True
        ).exists()

        if not is_member:
            return HttpResponseForbidden("You need to be a member of our Guild to do that.")
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
        if not request.user.is_authenticated:
            return HttpResponseForbidden("You need to be logged in to do that.")

        try:
            social_account = SocialAccount.objects.get(user=request.user)
        except SocialAccount.DoesNotExist:
            return HttpResponseForbidden("You need to be logged in with Discord to do that.")

        is_author = self.request.user == self.get_object().author
        is_admin = RoleMembership.objects.filter(
            user_id=social_account.uid,
            guild_id=settings.DISCORD_GUILD_ID,
            role_id=settings.DISCORD_ADMIN_ROLE_ID,
        ).exists()

        if not (is_author or is_admin):
            return HttpResponseForbidden("You need to be the guide's author to do that.")
        return super().dispatch(request, *args, **kwargs)


class AddRequestDiscordUserMixin:
    """
    Adds the `discord_user` context variable to a template which is
    constructed from the socialaccount attached to `request.user`.
    If the logged in user is anonymous, this is `None`.
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            context['discord_user'] = None
        else:
            try:
                context['discord_user'] = SocialAccount.objects.get(user=self.request.user)
            except SocialAccount.DoesNotExist:
                context['discord_user'] = None
        return context


class AddIsMemberContextMixin:
    """
    Adds `is_member` to the template context which
    specifies whether the request user is a member
    of the guild specified as `settings.DISCORD_GUILD_ID`.
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not self.request.user.is_authenticated:
            context['is_member'] = False
        else:
            try:
                social_account = SocialAccount.objects.get(user=self.request.user)
            except SocialAccount.DoesNotExist:
                context['is_member'] = False
            else:
                context['is_member'] = GuildMembership.objects.filter(
                    user_id=social_account.uid,
                    guild_id=settings.DISCORD_GUILD_ID,
                    is_member=True,
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
        if not self.request.user.is_authenticated:
            context['is_admin'] = False
        else:
            try:
                social_account = SocialAccount.objects.get(user=self.request.user)
            except SocialAccount.DoesNotExist:
                context['is_admin'] = False
            else:
                context['is_admin'] = RoleMembership.objects.filter(
                    user_id=social_account.uid,
                    guild_id=settings.DISCORD_GUILD_ID,
                    role_id=settings.DISCORD_ADMIN_ROLE_ID,
                ).exists()
        return context
