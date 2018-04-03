import os
from operator import attrgetter

import requests
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.utils.decorators import method_decorator
from django.views import generic

from .forms import GuideForm
from .models import Guide
from stats.models import Users as DiscordUser


class IndexView(generic.ListView):
    context_object_name = 'latest_guides'
    paginate_by = 10
    template_name = 'guides/index.html'

    def get_queryset(self):
        return Guide.objects.order_by('-pub_datetime')


class CreateView(generic.View):
    form_class = GuideForm
    template_name = 'guides/create.html'

    @method_decorator(user_passes_test(attrgetter('is_member')))
    def get(self, request, *_args, **_kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    @method_decorator(user_passes_test(attrgetter('is_member')))
    def post(self, request, *_args, **_kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            guide = form.save(commit=False)
            guide.author = request.user
            guide.save()

            webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
            detail_url = request.build_absolute_uri(reverse('guides:detail', kwargs={'pk': guide.id}))
            if webhook_url is not None:
                requests.post(webhook_url, json={
                    'username': 'Community Website',
                    'avatar_url': 'https://cdn.discordapp.com/emojis/410506329359253514.png?v=1',
                    'embeds': [{
                        'title': f'New Guide posted: "{guide.title}"',
                        'author': {
                          'name': guide.author.username,
                          'icon_url': DiscordUser.from_django_user(request.user).avatar_url
                        },
                        'url': detail_url,
                        'description': guide.overview,
                        'color': 0x0066CC
                    }]
                })
            return HttpResponseRedirect(detail_url)

        return render(request, self.template_name, {'form': form})


class DetailView(generic.DetailView):
    model = Guide
    template_name = 'guides/detail.html'
