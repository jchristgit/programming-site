from django.shortcuts import reverse
from django.test import TestCase


class AnonymousUserHomeTests(TestCase):
    """
    Scenario:
        - Anonymous User
        - accesses index
    """

    def test_index_status_200(self):
        resp = self.client.get(reverse("home:index"))
        self.assertEqual(resp.status_code, 200)

    def test_index_context_member_count_is_zero(self):
        resp = self.client.get(reverse("home:index"))
        self.assertEqual(resp.context["total_members"], 0)
