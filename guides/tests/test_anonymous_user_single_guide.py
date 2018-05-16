from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from guides.models import Guide
from . import INDEX_GUIDE_CONTEXT_NAME


class AnonymousUserSingleGuideTests(TestCase):
    """
    Scenario:
        - 1 existing Guide
        - Anonymous User accesses the site
    """

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user('testauthor', password='testpass')
        cls.guide = Guide.objects.create(
            title='test guide',
            overview="test guide overview",
            content="test guide content",
            author=cls.author
        )

    def test_index_status_200(self):
        resp = self.client.get(reverse("guides:index"))
        self.assertEqual(resp.status_code, 200)

    def test_detail_for_created_guide_status_200(self):
        resp = self.client.get(reverse("guides:detail", kwargs={"pk": self.guide.id}))
        self.assertEqual(resp.status_code, 200)

    def test_detail_for_unknown_guide_status_404(self):
        resp = self.client.get(reverse("guides:detail", kwargs={"pk": 2}))
        self.assertEqual(resp.status_code, 404)

    def test_index_context_is_only_created_guide(self):
        """
        A single guide was created, and no other
        data should appear within the guides
        context object on the index template.
        """

        resp = self.client.get(reverse("guides:index"))
        self.assertSequenceEqual(resp.context[INDEX_GUIDE_CONTEXT_NAME], [self.guide])

    def test_index_links_to_new_guide(self):
        """
        When a guide exists, the index page
        should include a link to it in its
        list of all guides.
        """

        resp = self.client.get(reverse("guides:index"))
        guide_link = reverse("guides:detail", kwargs={"pk": self.guide.id})
        self.assertIn(guide_link.encode("utf-8"), resp.content)

    def test_anonymous_user_create_guide_status_403(self):
        """
        Anonymous Users should get 403 Forbidden
        when attempting to access the form used
        to create a guide.
        """

        resp = self.client.get(reverse("guides:create"))
        self.assertEqual(resp.status_code, 403)

    def test_anonymous_user_edit_guide_status_403(self):
        """
        Anonymous Users should get 403 Forbidden
        when attempting to access the form used
        to edit a guide.
        """

        resp = self.client.get(reverse("guides:edit", kwargs={"pk": self.guide.id}))
        self.assertEqual(resp.status_code, 403)

    def test_anonymous_user_delete_guide_status_403(self):
        """
        Anonymous Users should get 403 Forbidden
        when attempting to access the form
        used to delete a guide.
        """

        resp = self.client.get(reverse("guides:delete", kwargs={"pk": self.guide.id}))
        self.assertEqual(resp.status_code, 403)
