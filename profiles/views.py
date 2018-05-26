from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.views import generic

from stats.models import RoleMembership
from .models import RestrictProcessing



class ProfileDetailView(UserPassesTestMixin, generic.DetailView):
    model = User

    raise_exception = True
    permission_denied_message = "You are not allowed to view this profile at the time."

    def test_func(self):
        """Test function used by `UserPassesTestMixin`.

        Used to disallow viewing profiles where users
        have set `restrict_processing` as required by GDPR.

        Returns:
            True:
                If the user whose profile is being visited
                does not have `restrict_processing` set or
                has it set to `False` (which is the default).
            False:
                If the user set `restrict_processing` to
                `True` through the profile change form,
                or the user visiting is the owner of the
                profile that is being visited.
        """

        profile_user = self.get_object()

        # The user should always be able to view their own profile.
        if self.request.user == profile_user:
            return True

        try:
            restrict_processing_row = RestrictProcessing.objects.get(user=profile_user)
        except RestrictProcessing.DoesNotExist:
            return True
        else:
            restricted = restrict_processing_row.restrict_processing
            # restricted == False: returns True, user can access
            # restricted == True: returns False, user can not access
            return not restricted

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['socialaccount'] = SocialAccount.objects.get(user=self.get_object())
        except SocialAccount.DoesNotExist:
            context['socialaccount'] = None
        return context


class RestrictProcessingUpdateView(UserPassesTestMixin, generic.UpdateView):
    model = RestrictProcessing
    fields = ('restrict_processing',)

    raise_exception = True
    permission_denied_message = "You are not allowed to update a profile that isn't yours."

    def test_func(self):
        return self.request.user == self.get_object().user

    def get_success_url(self):
        return reverse('profiles:detail', kwargs={'pk': self.request.user.id})


class ProfileDeleteView(UserPassesTestMixin, generic.DeleteView):
    model = User
    success_url = reverse_lazy('home:index')

    raise_exception = True
    permission_denied_message = "You are not allowed to delete a profile that isn't yours."

    def test_func(self):
        return self.request.user == self.get_object()
