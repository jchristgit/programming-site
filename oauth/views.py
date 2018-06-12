import requests
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView
)
from django.conf import settings

from .provider import DiscordWithGuildScopeProvider


class CustomDiscordOAuth2Adapter(OAuth2Adapter):
    """Extends the default Discord OAuth adapter to request guild data in addition to user data."""

    provider_id = DiscordWithGuildScopeProvider.id
    access_token_url = 'https://discordapp.com/api/oauth2/token'
    authorize_url = 'https://discordapp.com/api/oauth2/authorize'
    profile_url = 'https://discordapp.com/api/users/@me'
    guild_url = 'https://discordapp.com/api/users/@me/guilds'

    def complete_login(self, request, app, token, **kwargs):
        """Finish the user login, and add user & guild information."""

        headers = {
            'Authorization': f'Bearer {token.token}',
            'Content-Type': 'application/json'
        }
        profile_data = requests.get(self.profile_url, headers=headers).json()
        guild_data = requests.get(self.guild_url, headers=headers).json()

        if isinstance(guild_data, list):
            guild = next(
                (guild for guild in guild_data if guild['id'] == settings.DISCORD_GUILD_ID),
                None
            )
        else:
            guild = None

        extra_data = {
            'guild': guild,
            **profile_data
        }

        return self.get_provider().sociallogin_from_response(request, extra_data)


oauth2_login = OAuth2LoginView.adapter_view(CustomDiscordOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(CustomDiscordOAuth2Adapter)
