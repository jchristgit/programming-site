from django.test import TestCase
from django.urls import reverse

from . import INDEX_GUIDE_CONTEXT_NAME


class NoGuidesTests(TestCase):
    """
    Scenario:
        Empty database, meaning:
        - No Guide is present
        - No User is present
    """

    def test_index_status_200(self):
        resp = self.client.get(reverse("guides:index"))
        self.assertEqual(resp.status_code, 200)

    def test_detail_status_404(self):
        resp = self.client.get(reverse("guides:detail", kwargs={"pk": 1}))
        self.assertEqual(resp.status_code, 404)

    def test_no_guides_passes_empty_context_data(self):
        """
        Since no Guides exist in the database,
        the index page should receive an empty query
        set for the `guides` context object.
        """

        resp = self.client.get(reverse("guides:index"))
        context_guides = resp.context[INDEX_GUIDE_CONTEXT_NAME]

        self.assertFalse(context_guides.exists())
        self.assertSequenceEqual(context_guides, [])
