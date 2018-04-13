from django.conf import settings
from django.db import models
from markupfield.fields import MarkupField


class Guide(models.Model):
    title = models.CharField(
        max_length=100,
        help_text="Give your guide a readable and descriptive title."
    )
    overview = models.TextField(
        max_length=200,
        help_text="A short overview of the guide, used for preview information and in OGP tags."
    )
    content = MarkupField(
        markup_type='markdown',
        help_text="Markdown with fenced code blocks (GFM) is supported."
    )
    pub_datetime = models.DateTimeField(auto_now_add=True, editable=False)
    edit_datetime = models.DateTimeField(auto_now=True, editable=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    editors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        help_text=("Add editors to your Guide. You will always stay "
                   "the sole owner of it, and can add and remove editors freely."),
        related_name='+'
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-pub_datetime']
