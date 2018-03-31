from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from markupfield.fields import MarkupField


# Create your models here.
class Guide(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField(
        max_length=200,
        help_text="A short overview of the guide, used for preview information and in OGP tags."
    )
    content = MarkupField(markup_type='markdown')
    pub_datetime = models.DateTimeField(auto_now_add=True, editable=False)
    edit_datetime = models.DateTimeField(auto_now=True, editable=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
