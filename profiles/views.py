from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views import generic

from stats.models import RoleMembership


class ProfileDetailView(generic.DetailView):
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


class ProfileDeleteView(UserPassesTestMixin, generic.DeleteView):
    model = User
    success_url = reverse_lazy('home:index')

    raise_exception = True
    permission_denied_message = "You are not allowed to delete a profile that isn't yours."

    def test_func(self):
        return self.request.user == self.get_object()
