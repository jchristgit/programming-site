from django.shortcuts import reverse
from django.test import TestCase


class StatsTests(TestCase):

    def test_index_redirects_to_ddd(self):
        resp = self.client.get(reverse("stats:index"))
        self.assertRedirects(
            resp, "https://ddd.raylu.net", fetch_redirect_response=False
        )
