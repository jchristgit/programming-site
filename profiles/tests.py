from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import TestCase


class AnonymousUserProfilesTests(TestCase):
    """
    Scenario:
        - Anonymous User
        - accesses profile detail
    """

    def test_detail_status_404(self):
        resp = self.client.get(reverse("profiles:detail", kwargs={"pk": 214}))
        self.assertEqual(resp.status_code, 404)


class GuestUserProfilesTests(TestCase):
    """
    Scenario:
        - Guest User
        - accesses profile detail
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user('testuser', password='testpassword')

    def setUp(self):
        self.client.force_login(self.user)

    def test_detail_status_200(self):
        resp = self.client.get(reverse("profiles:detail", kwargs={"pk": self.user.id}))
        self.assertEqual(resp.status_code, 200)

    def test_detail_context(self):
        resp = self.client.get(reverse("profiles:detail", kwargs={"pk": self.user.id}))
        self.assertEqual(resp.context["user"], self.user)
