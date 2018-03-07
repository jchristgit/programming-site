from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    avatar_hash = models.CharField(max_length=32)
    discriminator = models.IntegerField()
    is_member = models.BooleanField(default=False)

    def get_avatar_url(self):
        if self.avatar_hash:
            return f'https://cdn.discordapp.com/avatars/{self.id}/{self.avatar_hash}.png'
        return 'https://cdn.discordapp.com/emojis/294873283017310208.png'

    class Meta:
        unique_together = ('username', 'discriminator')
