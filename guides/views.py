from django.views import generic

from .models import Guide


class IndexView(generic.ListView):
    context_object_name = 'latest_guides'
    template_name = 'guides/index.html'

    def get_queryset(self):
        return Guide.objects.order_by('-pub_datetime')
