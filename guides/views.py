from operator import attrgetter

from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.utils.decorators import method_decorator
from django.views import generic

from .forms import GuideForm
from .models import Guide


class IndexView(generic.ListView):
    context_object_name = 'latest_guides'
    template_name = 'guides/index.html'

    def get_queryset(self):
        return Guide.objects.order_by('-pub_datetime')


class CreateView(generic.View):
    form_class = GuideForm
    template_name = 'guides/create.html'

    @method_decorator(user_passes_test(attrgetter('is_member')))
    def get(self, request, *_args, **_kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    @method_decorator(user_passes_test(attrgetter('is_member')))
    def post(self, request, *_args, **_kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            guide = form.save(commit=False)
            guide.author = request.user
            guide.save()
            return HttpResponseRedirect(reverse('guides:detail', kwargs={'pk': guide.id}))

        return render(request, self.template_name, {'form': form})


class DetailView(generic.DetailView):
    model = Guide
    template_name = 'guides/detail.html'
