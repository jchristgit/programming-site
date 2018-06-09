# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django
#     to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.conf import settings
from django.db import models


class AuditLog(models.Model):
    audit_entry_id = models.BigAutoField(primary_key=True)
    guild_id = models.BigIntegerField()
    action = models.TextField()  # This field type is a guess.
    user = models.ForeignKey("Users", models.DO_NOTHING)
    reason = models.TextField(blank=True, null=True)
    # This field type is a guess.
    category = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "audit_log"


class AuditLogChanges(models.Model):
    audit_entry = models.OneToOneField(AuditLog, models.DO_NOTHING, primary_key=True)
    guild_id = models.BigIntegerField()
    state = models.TextField()  # This field type is a guess.
    attributes = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = "audit_log_changes"
        unique_together = (("audit_entry", "state"),)


class AuditLogCrawl(models.Model):
    guild_id = models.BigIntegerField(primary_key=True)
    last_audit_entry_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = "audit_log_crawl"


class ChannelCategories(models.Model):
    category_id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    position = models.IntegerField()
    is_deleted = models.BooleanField()
    is_nsfw = models.BooleanField()
    changed_roles = models.TextField()  # This field type is a guess.
    parent_category = models.ForeignKey(
        "self", models.DO_NOTHING, blank=True, null=True
    )
    guild_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = "channel_categories"


# Unable to inspect table 'channel_crawl'
# The error was: permission denied for relation channel_crawl


class Channels(models.Model):
    channel_id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    is_nsfw = models.BooleanField()
    is_deleted = models.BooleanField()
    position = models.IntegerField()
    topic = models.TextField(blank=True, null=True)
    changed_roles = models.TextField()  # This field type is a guess.
    category = models.ForeignKey(
        ChannelCategories, models.DO_NOTHING, blank=True, null=True
    )
    guild_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = "channels"


class Emojis(models.Model):
    emoji_id = models.BigIntegerField()
    emoji_unicode = models.CharField(max_length=7)
    is_custom = models.BooleanField()
    is_managed = models.NullBooleanField()
    is_deleted = models.BooleanField()
    name = models.TextField()  # This field type is a guess.
    category = models.TextField()  # This field type is a guess.
    # This field type is a guess.
    roles = models.TextField(blank=True, null=True)
    guild_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "emojis"
        unique_together = (("emoji_id", "emoji_unicode"),)


class GuildMembership(models.Model):
    user = models.OneToOneField("Users", models.DO_NOTHING, primary_key=True)
    guild_id = models.BigIntegerField()
    is_member = models.BooleanField()
    joined_at = models.DateTimeField(blank=True, null=True)
    nick = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "guild_membership"
        unique_together = (("user", "guild_id"),)


class Guilds(models.Model):
    guild_id = models.BigAutoField(primary_key=True)
    owner = models.ForeignKey("Users", models.DO_NOTHING)
    name = models.TextField()
    icon = models.TextField()
    voice_region = models.TextField()  # This field type is a guess.
    afk_channel_id = models.BigIntegerField(blank=True, null=True)
    afk_timeout = models.IntegerField()
    mfa = models.BooleanField()
    verification_level = models.TextField()  # This field type is a guess.
    explicit_content_filter = models.TextField()  # This field type is a guess.
    features = models.TextField()  # This field type is a guess.
    splash = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "guilds"


class Mentions(models.Model):
    mentioned_id = models.BigIntegerField(primary_key=True)
    type = models.TextField()  # This field type is a guess.
    message = models.ForeignKey("Messages", models.DO_NOTHING)
    channel = models.ForeignKey(Channels, models.DO_NOTHING)
    guild_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = "mentions"
        unique_together = (("mentioned_id", "type", "message"),)


class Messages(models.Model):
    message_id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    edited_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    message_type = models.TextField()  # This field type is a guess.
    system_content = models.TextField()
    content = models.TextField()
    embeds = models.TextField()
    attachments = models.IntegerField()
    webhook_id = models.BigIntegerField(blank=True, null=True)
    user_id = models.BigIntegerField()
    channel = models.ForeignKey(Channels, models.DO_NOTHING)
    guild_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = "messages"


class Pins(models.Model):
    pin_id = models.BigIntegerField(primary_key=True)
    message = models.ForeignKey(Messages, models.DO_NOTHING)
    pinner = models.ForeignKey("Users", models.DO_NOTHING, related_name="pinner")
    user = models.ForeignKey("Users", models.DO_NOTHING)
    channel = models.ForeignKey(Channels, models.DO_NOTHING)
    guild_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = "pins"
        unique_together = (("pin_id", "message"),)


class Reactions(models.Model):
    message_id = models.BigIntegerField()
    emoji_id = models.BigIntegerField()
    emoji_unicode = models.CharField(max_length=7)
    user = models.ForeignKey("Users", models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    channel = models.ForeignKey(Channels, models.DO_NOTHING)
    guild_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = "reactions"
        unique_together = (
            ("message_id", "emoji_id", "emoji_unicode", "user", "created_at"),
        )


class RoleMembership(models.Model):
    role = models.OneToOneField("Roles", models.DO_NOTHING, primary_key=True)
    guild_id = models.BigIntegerField()
    user = models.OneToOneField("Users", models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = "role_membership"
        unique_together = (("role", "user"),)


class Roles(models.Model):
    role_id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    color = models.IntegerField()
    raw_permissions = models.BigIntegerField()
    guild_id = models.BigIntegerField()
    is_hoisted = models.BooleanField()
    is_managed = models.BooleanField()
    is_mentionable = models.BooleanField()
    is_deleted = models.BooleanField()
    position = models.IntegerField()

    class Meta:
        managed = False
        db_table = "roles"


class Typing(models.Model):
    timestamp = models.DateTimeField()
    user = models.ForeignKey("Users", models.DO_NOTHING)
    channel = models.ForeignKey(Channels, models.DO_NOTHING)
    guild_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = "typing"
        unique_together = (("timestamp", "user", "channel", "guild_id"),)


class Users(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    discriminator = models.IntegerField()
    avatar = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField()
    is_bot = models.BooleanField()

    class Meta:
        managed = False
        db_table = "users"

    def avatar_url(self, size=64):
        return f"https://cdn.discordapp.com/avatars/{self.user_id}/{self.avatar}.png?size={size}"


class VoiceChannels(models.Model):
    voice_channel_id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    is_deleted = models.BooleanField()
    position = models.IntegerField()
    bitrate = models.IntegerField()
    user_limit = models.IntegerField()
    changed_roles = models.TextField()  # This field type is a guess.
    category = models.ForeignKey(
        ChannelCategories, models.DO_NOTHING, blank=True, null=True
    )
    guild_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = "voice_channels"
