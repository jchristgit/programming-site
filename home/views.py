from django.contrib.auth.models import User
from django.shortcuts import render
from django.views import generic

from stats.models import (
    GuildMembership,
    Users as DiscordUser
)


class IndexView(generic.View):
    template_name = 'home/index.html'

    def get(self, request):
        total_members = GuildMembership.objects.using('stats').filter(
            guild_id=181866934353133570, is_member=True
        ).count()

        context = {
            'total_members': total_members
        }
        return render(request, self.template_name, context)


class ProfileView(generic.DetailView):
    model = User
    template_name = 'home/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['discord_user'] = DiscordUser.from_django_user(context['user'])
        return context
