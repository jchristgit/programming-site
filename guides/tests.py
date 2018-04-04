import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Guide
from .views import IndexView


INDEX_GUIDE_CONTEXT_NAME = IndexView.context_object_name


class GuidesModelNoGuidesTests(TestCase):
    def test_index_status_200(self):
        resp = self.client.get(reverse('guides:index'))
        self.assertEqual(resp.status_code, 200)

    def test_detail_status_404(self):
        resp = self.client.get(reverse('guides:detail', kwargs={'pk': 1}))
        self.assertEqual(resp.status_code, 404)

    def test_no_guides_passes_empty_context_data(self):
        resp = self.client.get(reverse('guides:index'))
        context_guides = resp.context[INDEX_GUIDE_CONTEXT_NAME]

        self.assertFalse(context_guides.exists())
        self.assertSequenceEqual(context_guides, [])



