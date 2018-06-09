import requests
from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.urls import reverse_lazy
from django.views import generic
from guardian.mixins import PermissionRequiredMixin

from .models import Guide


class IndexView(generic.ListView):
    context_object_name = "latest_guides"
    model = Guide
    paginate_by = 10


class DetailView(generic.DetailView):
    model = Guide


class CreateView(PermissionRequiredMixin, generic.CreateView):
    fields = ['title', 'overview', 'content']
    model = Guide

    permission_required = 'guides.add_guide'
    permission_object = None
    return_403 = True

    def form_valid(self, form):
        guide = form.save(commit=False)
        guide.author = self.request.user
        guide.save()

        detail_url = self.request.build_absolute_uri(
            reverse("guides:detail", kwargs={"pk": guide.id})
        )
        if settings.DISCORD_WEBHOOK_URL is not None and not settings.IS_TESTING:
            discord_user = SocialAccount.objects.filter(user=self.request.user).first()
            if discord_user is not None:
                requests.post(
                    settings.DISCORD_WEBHOOK_URL,
                    json={
                        "embeds": [
                            {
                                "title": f'New Guide posted: "{guide.title}"',
                                "author": {
                                    "name": guide.author.username,
                                    "icon_url": discord_user.get_avatar_url()
                                },
                                "url": detail_url,
                                "description": guide.overview,
                                "color": 0x0066CC
                            }
                        ]
                    }
                )
        return HttpResponseRedirect(detail_url)


class EditView(PermissionRequiredMixin, generic.UpdateView):
    fields = ['title', 'overview', 'content']
    model = Guide

    permission_required = 'guides.change_guide'
    accept_global_perms = True
    return_403 = True

    def get_success_url(self):
        return reverse("guides:detail", kwargs={"pk": self.object.id})

    def form_valid(self, form):
        super().form_valid(form)
        detail_url = self.request.build_absolute_uri(
            reverse("guides:detail", kwargs={"pk": self.object.id})
        )
        return HttpResponseRedirect(detail_url)


class DeleteView(PermissionRequiredMixin, generic.DeleteView):
    model = Guide
    success_message = 'The guide "{}" was deleted successfully.'
    success_url = reverse_lazy("guides:index")

    permission_required = 'guides.delete_guide'
    accept_global_perms = True
    return_403 = True

    def delete(self, *args, **kwargs):
        messages.success(
            self.request, self.success_message.format(self.get_object().title)
        )
        return super().delete(*args, **kwargs)
