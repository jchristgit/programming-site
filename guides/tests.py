import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Guide
from .views import IndexView


GUIDE_CONTEXT_NAME = IndexView.context_object_name


class GuidesModelNoGuidesTests(TestCase):
    def test_index_status_200(self):
        self.assertEqual(self.client.get(reverse('guides:index')).status_code, 200)

    def test_no_guides_passes_empty_context_data(self):
        res = self.client.get(reverse('guides:index'))
        context_guides = res.context[GUIDE_CONTEXT_NAME]

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
        ),
        cls.guide_2 = Guide.objects.create(
            title="Test Guide 2", overview="test",
            content="test", author=cls.author,
            pub_datetime=past
        )

    def test_index_status_200(self):
        self.assertEqual(self.client.get(reverse('guides:index')).status_code, 200)

    def test_guide_context_data_is_sorted(self):
        res = self.client.get(reverse('guides:index'))
        context_guides = res.context[GUIDE_CONTEXT_NAME]

        self.assertGreater(context_guides[0].pub_datetime, context_guides[1].pub_datetime)
