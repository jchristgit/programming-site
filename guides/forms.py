from django.forms import ModelForm

from .models import Guide


class GuideForm(ModelForm):
    class Meta:
        model = Guide
        fields = ['title', 'overview', 'content']
