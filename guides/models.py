from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Guide(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField(
        max_length=200,
        help_text="A short overview of the guides, used for preview information and in OGP tags."
    )
    content = models.TextField()
    pub_datetime = models.DateTimeField(auto_now_add=True, editable=False)
    edit_datetime = models.DateTimeField(auto_now=True, editable=False)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
