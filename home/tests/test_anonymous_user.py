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
