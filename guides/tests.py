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


class GuidesModelExistingGuidesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        past = datetime.datetime(1982, 12, 5, 1, 4, 2, 3)
        now = datetime.datetime.now()
        cls.author = get_user_model().objects.create_user(
            "test", "test@test.com", "testpassword", discriminator=0000
        )
        cls.guide_1 = Guide.objects.create(
            title="Test Guide", overview="test",
            content="test", author=cls.author,
            pub_datetime=now
        )
        cls.guide_2 = Guide.objects.create(
            title="Test Guide 2", overview="test",
            content="test", author=cls.author,
            pub_datetime=past
        )

    def test_index_status_200(self):
        self.assertEqual(self.client.get(reverse('guides:index')).status_code, 200)

    def test_detail_status_200(self):
        for guide in [self.guide_1, self.guide_2]:
            resp = self.client.get(reverse('guides:detail', kwargs={'pk': guide.id}))
            self.assertEqual(resp.status_code, 200)

    def test_index_context_contains_created_guides(self):
        resp = self.client.get(reverse('guides:index'))
        self.assertIn(self.guide_1, resp.context[INDEX_GUIDE_CONTEXT_NAME])
        self.assertIn(self.guide_2, resp.context[INDEX_GUIDE_CONTEXT_NAME])

    def test_index_context_guides_sorted(self):
        resp = self.client.get(reverse('guides:index'))
        context_guides = resp.context[INDEX_GUIDE_CONTEXT_NAME]

        self.assertGreater(context_guides[0].pub_datetime, context_guides[1].pub_datetime)


class AnonymousUserGuidesTests(TestCase):
    def test_create_get_status_302(self):
        resp = self.client.get(reverse('guides:create'))
        self.assertEqual(resp.status_code, 302)

    def test_create_post_status_302(self):
        resp = self.client.post(reverse('guides:create'))
        self.assertEqual(resp.status_code, 302)
