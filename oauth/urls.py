from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from django.urls import path
from django.views.generic import TemplateView

from .provider import DiscordWithGuildScopeProvider


urlpatterns = default_urlpatterns(DiscordWithGuildScopeProvider)
urlpatterns.append(
    path(
        'prelogin',
        TemplateView.as_view(template_name='oauth/prelogin.html'),
        name='prelogin'
    )
)
