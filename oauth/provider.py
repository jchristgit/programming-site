from allauth.socialaccount.providers import registry
from allauth.socialaccount.providers.discord.provider import DiscordAccount, DiscordProvider


SCOPE = ('identify', 'guilds')


class CustomDiscordAccount(DiscordAccount):
    """Represents a Discord account obtained from OAuth2 data.

    Extends the default methods provided by the built-in
    Discord OAuth provider integration with a few new ones.
    """

    def get_avatar_url(self):
        """Returns the avatar URL of this account.

        This also takes into account if the user has
        no avatar set explicitly, and returns the
        corresponding default avatar from Discord instead.
        """

        if 'avatar' in self.account.extra_data:
            avatar_hash = self.account.extra_data['avatar']
            user_id = self.account.extra_data['id']
            return f'https://cdn.discordapp.com/avatars/{user_id}/{avatar_hash}.png'

        discriminator = self.account.extra_data['discriminator']
        return f'https://cdn.discordapp.com/embed/avatars/{discriminator % 5}.png'

    def get_profile_url(self):
        """Returns a link to open a direct message to this account."""

        user_id = self.account.extra_data['id']
        return f'https://discordapp.com/channels/@me/{user_id}'


class DiscordWithGuildScopeProvider(DiscordProvider):
    """Changes the default Discord OAuth2 adapter to use the ('identify', 'guilds') scope."""

    id = 'discoauth'
    account_class = CustomDiscordAccount

    def extract_common_fields(self, data):
        return {
            'username': data.get('username'),
            'name': data.get('username')
        }

    def get_default_scope(self):
        return SCOPE


registry.register(DiscordWithGuildScopeProvider)
