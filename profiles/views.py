from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views import generic


class ProfileDetailView(generic.DetailView):
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['socialaccount'] = SocialAccount.objects.get(user=self.get_object())
        except SocialAccount.DoesNotExist:
            context['socialaccount'] = None
        return context


class ProfileDeleteView(UserPassesTestMixin, generic.DeleteView):
    model = User
    success_url = reverse_lazy('home:index')

    raise_exception = True
    permission_denied_message = "You are not allowed to delete a profile that isn't yours."

    def test_func(self):
        return self.request.user == self.get_object()
