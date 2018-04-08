from django.contrib.auth.models import User
from django.conf import settings
from django.views import generic

from stats.models import GuildMembership


class IndexView(generic.TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_members'] = GuildMembership.objects.using('stats').filter(
            guild_id=settings.DISCORD_GUILD_ID, is_member=True
        ).count()
        return context


class ProfileView(generic.DetailView):
    model = User
