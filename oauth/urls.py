from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns

from .provider import DiscordWithGuildScopeProvider


urlpatterns = default_urlpatterns(DiscordWithGuildScopeProvider)
