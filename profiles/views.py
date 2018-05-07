from django.conf import settings
from django.contrib.auth.models import User
from django.views import generic

from stats.models import RoleMembership


class ProfileView(generic.DetailView):
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["discord_role_membership"] = RoleMembership.objects.filter(
            guild_id=settings.DISCORD_GUILD_ID, user_id=self.get_object().id
        ).order_by(
            "-role__position"
        ).exclude(
            role__name="@everyone"
        )
        return context
