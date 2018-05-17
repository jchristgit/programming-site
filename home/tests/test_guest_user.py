from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import TestCase


class GuestUserHomeTests(TestCase):
    """
    Scenario:
        - Guest User
        - accesses index
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user('testuser', password='testpassword')

    def setUp(self):
        self.client.force_login(self.user)

    def test_index_status_200(self):
        resp = self.client.get(reverse("home:index"))
        self.assertEqual(resp.status_code, 200)

    def test_index_context_member_count_is_zero(self):
        resp = self.client.get(reverse("home:index"))
        self.assertEqual(resp.context["total_members"], 0)
