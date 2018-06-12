from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse

from guides.models import Guide
from . import INDEX_GUIDE_CONTEXT_NAME


@override_settings(DISCORD_GUILD_ID=55555)
class AuthorUserSingleGuideTests(TestCase):
    """
    Scenario:
        - 1 existing Guide
        - Author (also Member) of the Guide accesses the site
    """

    multi_db = True

    @classmethod
    def setUpTestData(cls):
        discord_user_id = 42

        cls.author = User.objects.create_user('testauthor', password='testpass')
        cls.guide = Guide.objects.create(
            title="test guide",
            overview="test overview",
            content="test guide content",
            author=cls.author
        )
        cls.social_account = SocialAccount.objects.create(
            user=cls.author,
            uid=discord_user_id,
            extra_data={'guild': {'id': '55555', 'permissions': 0x63584C0}}
        )

    def setUp(self):
        self.client.force_login(self.author)

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

    def test_author_user_get_create_guide_status_200(self):
        """
        The guide author is a member and therefore
        should be allowed to create a Guide,
        thus `guides:create` should respond with 200 OK.
        The `DISCORD_GUILD_ID` setting needs to be
        overridden since the `MemberRequiredMixin`
        used by `guides:create` uses this value to
        determine whether the request was made by a member.
        """

        resp = self.client.get(reverse("guides:create"))
        self.assertEqual(resp.status_code, 200)

    def test_author_user_get_edit_guide_status_200(self):
        """
        The author should get 200 OK when attempting
        to GET `guides:edit` the guide that they created.
        """

        resp = self.client.get(reverse("guides:edit", kwargs={"pk": self.guide.id}))
        self.assertEqual(resp.status_code, 200)

    def test_member_user_get_delete_guide_status_200(self):
        """
        The author should get 200 OK when attempting
        to GET `guides:delete` for a guide they created.
        """

        resp = self.client.get(reverse("guides:delete", kwargs={"pk": self.guide.id}))
        self.assertEqual(resp.status_code, 200)
