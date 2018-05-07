from django import forms
from django.conf import settings
from django.contrib.auth.models import User

from stats.models import GuildMembership
from .models import Guide


class GuideForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

        self.fields["editors"] = forms.ModelMultipleChoiceField(
            queryset=User.objects.filter(
                id__in=set(
                    GuildMembership.objects.using("stats").filter(
                        guild_id=settings.DISCORD_GUILD_ID, is_member=True
                    ).values_list(
                        "user_id", flat=True
                    )
                )
            ).exclude(
                id=user.id
            ).order_by(
                "first_name"
            ),
            required=False,
            help_text=Guide._meta.get_field("editors").help_text,
        )

    class Meta:
        fields = ["title", "overview", "editors", "content"]
        model = Guide
