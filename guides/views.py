import requests
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.urls import reverse_lazy
from django.views import generic

from .models import Guide
from stats.models import Users as DiscordUser
from website.mixins import (
    AddIsMemberContextMixin,
    AddIsAdminContextMixin,
    AuthorRequiredMixin,
    MemberRequiredMixin
)


class IndexView(AddIsMemberContextMixin, AddIsAdminContextMixin, generic.ListView):
    context_object_name = 'latest_guides'
    paginate_by = 10

    def get_queryset(self):
        return Guide.objects.order_by('-pub_datetime')


class DetailView(generic.DetailView):
    model = Guide

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author_discord'] = DiscordUser.from_django_user(self.request.user)
        return context


class CreateView(MemberRequiredMixin, generic.CreateView):
    fields = ['title', 'overview', 'content']
    model = Guide

    def form_valid(self, form):
        guide = form.save(commit=False)
        guide.author = self.request.user
        guide.save()

        detail_url = self.request.build_absolute_uri(reverse('guides:detail', kwargs={'pk': guide.id}))
        if settings.DISCORD_WEBHOOK_URL is not None:
            requests.post(settings.DISCORD_WEBHOOK_URL, json={
                'embeds': [{
                    'title': f'New Guide posted: "{guide.title}"',
                    'author': {
                        'name': guide.author.username,
                        'icon_url': DiscordUser.from_django_user(self.request.user).avatar_url
                    },
                    'url': detail_url,
                    'description': guide.overview,
                    'color': 0x0066CC
                }]
            })
        return HttpResponseRedirect(detail_url)


class EditView(MemberRequiredMixin, AuthorRequiredMixin, generic.UpdateView):
    fields = ['title', 'overview', 'content']
    model = Guide

    def get_success_url(self):
        return reverse('guides:detail', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        detail_url = self.request.build_absolute_uri(reverse('guides:detail', kwargs={'pk': self.object.id}))
        if settings.DISCORD_WEBHOOK_URL is not None:
            requests.post(settings.DISCORD_WEBHOOK_URL, json={
                'embeds': [{
                    'title': f'{self.object.author}\'s guide "{self.object.title}" was just updated!',
                    'author': {
                        'name': self.request.user.username,
                        'icon_url': DiscordUser.from_django_user(self.request.user).avatar_url
                    },
                    'url': detail_url,
                    'color': 0x0099FF
                }]
            })
        return HttpResponseRedirect(detail_url)


class DeleteView(MemberRequiredMixin, AuthorRequiredMixin, generic.DeleteView):
    model = Guide
    success_message = 'The guide "{}" was deleted successfully.'
    success_url = reverse_lazy('guides:index')

    def delete(self, *args, **kwargs):
        messages.success(self.request, self.success_message.format(self.get_object().title))
        return super().delete(*args, **kwargs)

    def form_valid(self, form):
        author_profile = self.request.build_absolute_uri(reverse('home:profile', kwargs={'pk': self.object.author.id}))
        if settings.DISCORD_WEBHOOK_URL is not None:
            requests.post(settings.DISCORD_WEBHOOK_URL, json={
                'embeds': [{
                    'title': f'{self.object.author}\'s guide "{self.object.title}" was deleted.',
                    'author': {
                        'name': self.request.user.username,
                        'icon_url': DiscordUser.from_django_user(self.request.user).avatar_url
                    },
                    'url': author_profile,
                    'color': 0xFF3300
                }]
            })
        return HttpResponseRedirect(author_profile)
