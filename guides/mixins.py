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
        guide = self.get_object()

        is_author = self.request.user == guide.author
        is_admin = RoleMembership.objects.using("stats").filter(
            user_id=request.user.id,
            guild_id=settings.DISCORD_GUILD_ID,
            role_id=settings.DISCORD_ADMIN_ROLE_ID,
        ).exists()
        is_editor = guide.editors.filter(id=self.request.user.id).exists()

        if not (is_author or is_admin or is_editor):
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)
