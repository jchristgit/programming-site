from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from django.http import HttpResponseForbidden

from stats.models import RoleMembership


class AuthorOrEditorRequiredMixin:
    """
    Checks that the user associated with the request
    is the author or editor of the guide captured within it,
    or alternatively is an admin - this is checked
    by testing their role membership against `DISCORD_ADMIN_ROLE_ID`
    from the settings. If these fail, returns Forbidden.
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("You need to be logged in to do that.")

        guide = self.get_object()

        try:
            social_account = SocialAccount.objects.get(user=self.request.user)
        except SocialAccount.DoesNotExist:
            return HttpResponseForbidden()

        is_author = self.request.user == guide.author
        is_admin = RoleMembership.objects.filter(
            user_id=social_account.uid,
            guild_id=settings.DISCORD_GUILD_ID,
            role_id=settings.DISCORD_ADMIN_ROLE_ID,
        ).exists()

        if not (is_author or is_admin):
            return HttpResponseForbidden("You need to be the author of this guide to edit it.")
        return super().dispatch(request, *args, **kwargs)
