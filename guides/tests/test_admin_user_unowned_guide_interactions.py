from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse

from guides.models import Guide
from stats.models import RoleMembership, Roles, Users as DiscordUser
from . import INDEX_GUIDE_CONTEXT_NAME


@override_settings(
    DISCORD_ADMIN_ROLE_ID=30,
    DISCORD_GUILD_ID=55555
)
class AdminUserUnownedGuideInteractionsTests(TestCase):
    """
    Scenario:
        - 1 existing Guide
        - (Discord) administrator accesses the site
        - (Discord) administrator uses guide creation, edit, and delete views
          for guides not owned by them
    """

    multi_db = True

    @classmethod
    def setUpTestData(cls):
        discord_user_id = 42
        discord_guild_id = 55555

        cls.author = User.objects.create_user('testauthor', password='testpass')
        cls.guide = Guide.objects.create(
            title="test guide",
            overview="test overview",
            content="test guide content",
            author=cls.author
        )

        cls.admin_user = User.objects.create_user('testadmin', password='testpass')
        cls.staff_role = Roles.objects.create(
            role_id=30,
            name='test staff role',
            color=0,
            raw_permissions=0,
            guild_id=discord_guild_id,
            is_hoisted=False,
            is_managed=False,
            is_mentionable=False,
            is_deleted=False,
            position=0
        )
        cls.discord_user = DiscordUser.objects.create(
            user_id=discord_user_id,
            name='test admin user',
            discriminator=0000,
            is_deleted=False,
            is_bot=False
        )
        cls.role_membership = RoleMembership.objects.create(
            role=cls.staff_role,
            guild_id=discord_guild_id,
            user=cls.discord_user
        )
        cls.social_account = SocialAccount.objects.create(
            user=cls.admin_user,
            uid=discord_user_id,
            extra_data={}
        )

    def setUp(self):
        self.client.force_login(self.admin_user)

    def test_staff_can_edit_unowned_guide(self):
        """
        A staff member should be able to edit
        a guide that they do not own, and
        editing the guide should redirect them
        towards the detail page for it.
        """

        edit_data = {
            "title": "edited title",
            "overview": "edited overview",
            "content": "edited content",
        }
        guide_edit_post = self.client.post(
            reverse("guides:edit", kwargs={"pk": self.guide.id}), data=edit_data
        )
        self.guide.refresh_from_db()

        guide_edit_get = self.client.get(
            reverse("guides:edit", kwargs={"pk": self.guide.id})
        )
        self.assertEqual(guide_edit_get.status_code, 200)

        self.assertEqual(guide_edit_post.status_code, 302)
        self.assertEqual(self.guide.title, edit_data["title"])
        self.assertEqual(self.guide.overview, edit_data["overview"])
        self.assertEqual(self.guide.content.raw, edit_data["content"])
        self.assertTrue(
            guide_edit_post.url.endswith(
                reverse("guides:detail", kwargs={"pk": self.guide.id})
            )
        )

        guide_detail = self.client.get(
            reverse("guides:detail", kwargs={"pk": self.guide.id})
        )
        self.assertEqual(guide_detail.context["guide"], self.guide)

    def test_staff_can_delete_unowned_guide(self):
        """
        A staff member should be able to delete
        a guide that they do not own, and
        deleting the guide should redirect them
        towards `guides:index`.
        """

        guide_delete_get = self.client.get(
            reverse("guides:delete", kwargs={"pk": self.guide.id})
        )
        self.assertEqual(guide_delete_get.status_code, 200)

        guide_delete_post = self.client.post(
            reverse("guides:delete", kwargs={"pk": self.guide.id})
        )
        self.assertIsNone(Guide.objects.first())
        self.assertTrue(guide_delete_post.url.endswith(reverse("guides:index")))

        guide_index = self.client.get(reverse("guides:index"))
        self.assertSequenceEqual(guide_index.context[INDEX_GUIDE_CONTEXT_NAME], [])
