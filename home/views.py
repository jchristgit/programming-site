from django.contrib.auth.models import User
from django.conf import settings
from django.shortcuts import render
from django.views import generic

from stats.models import GuildMembership
from website.mixins import (
    AddIsAdminContextMixin,
    AddIsMemberContextMixin,
    AddRequestDiscordUserMixin
)


class IndexView(generic.View):
    template_name = 'home/index.html'

    def get(self, request):
        total_members = GuildMembership.objects.using('stats').filter(
            guild_id=settings.DISCORD_GUILD_ID, is_member=True
        ).count()
        context = {
            'total_members': total_members
        }
        return render(request, self.template_name, context)


class ProfileView(AddIsAdminContextMixin, AddIsMemberContextMixin,
                  AddRequestDiscordUserMixin, generic.DetailView):
    model = User
    template_name = 'home/profile.html'
