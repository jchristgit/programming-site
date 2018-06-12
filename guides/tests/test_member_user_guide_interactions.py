from datetime import datetime

from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse

from guides.models import Guide


@override_settings(DISCORD_GUILD_ID=55555)
class MemberUserGuideInteractionsTests(TestCase):
    """
    Scenario:
        - 1 existing Guide
        - Member accesses the site
        - Member uses guide creation, edit, and deletion views
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user('testmember', password='testpass')
        cls.social_account = SocialAccount.objects.create(
            user=cls.user,
            uid=42,
            extra_data={'guild': {'id': '55555', 'permissions': 0x63584C0}}
        )
        cls.guide_data = {
            "title": "test guide",
            "overview": "test guide overview",
            "content": "test guide content",
        }
        edit_data = cls.guide_data.copy()
        edit_data["title"] = "Edited test guide"
        cls.guide_data_edit = edit_data

    def setUp(self):
        self.client.force_login(self.user)

    def test_member_user_can_create_guide(self):
        """
        A guild member should be able to create a Guide,
        and should get redirected to it after creation.
        """

        guide_create_post = self.client.post(
            reverse("guides:create"), data=self.guide_data
        )
        self.assertEqual(guide_create_post.status_code, 302)

        guide = Guide.objects.first()
        self.assertEqual(guide.title, self.guide_data["title"])
        self.assertEqual(guide.overview, self.guide_data["overview"])
        self.assertEqual(guide.content.raw, self.guide_data["content"])
        self.assertEqual(guide.author, self.user)

        self.assertIn(
            reverse("guides:detail", kwargs={"pk": guide.id}), guide_create_post.url
        )

    def test_member_user_can_edit_owned_guide(self):
        """
        A guild member should be able to
        edit a guide that they created,
        and saving the edit should redirect
        them to the detail view for the guide.
        """

        self.client.post(reverse("guides:create"), data=self.guide_data)
        guide = Guide.objects.first()
        guide_edit_get = self.client.get(
            reverse("guides:edit", kwargs={"pk": guide.id})
        )
        self.assertEqual(guide_edit_get.status_code, 200)

        guide_edit_post = self.client.post(
            reverse("guides:edit", kwargs={"pk": guide.id}), data=self.guide_data_edit
        )
        guide.refresh_from_db()
        self.assertEqual(guide_edit_post.status_code, 302)
        self.assertEqual(guide.title, self.guide_data_edit["title"])
        self.assertEqual(guide.overview, self.guide_data_edit["overview"])
        self.assertEqual(guide.content.raw, self.guide_data_edit["content"])
        self.assertEqual(guide.author, self.user)

        self.assertTrue(
            guide_edit_post.url.endswith(
                reverse("guides:detail", kwargs={"pk": guide.id})
            )
        )

    def test_member_user_can_delete_owned_guide(self):
        """
        A guild member should be able to
        delete a guide that they created,
        and saving the deletion should
        redirect them back to the guide index.
        Additionally, trying to access the
        detail page for the created guide
        after deletion should return 404.
        """

        self.client.post(reverse("guides:create"), data=self.guide_data)
        guide = Guide.objects.first()

        guide_delete_get = self.client.get(
            reverse("guides:delete", kwargs={"pk": guide.id})
        )
        self.assertEqual(guide_delete_get.status_code, 200)

        guide_delete_post = self.client.post(
            reverse("guides:delete", kwargs={"pk": guide.id})
        )
        self.assertEqual(guide_delete_post.status_code, 302)
        self.assertTrue(guide_delete_post.url.endswith(reverse("guides:index")))

        guide_detail_get = self.client.get(
            reverse("guides:detail", kwargs={"pk": guide.id})
        )
        self.assertEqual(guide_detail_get.status_code, 404)

    def test_member_cannot_change_excluded_fields_on_creation(self):
        """
        A bunch of fields are not supposed to be editable
        by the members, albeit being visible elsewhere -
        for example, the author ID or creation / publication
        date. We ensure here that the member cannot tamper
        with any of that data by submitting it anyways despite
        not being in the HTML form.
        """

        tampered_creation_date = datetime.utcnow()
        post_data = {
            'id': 41092,
            'title': "test guide",
            'overview': "test guide overview",
            'content': "test guide content",
            'author_id': 13920,
            'pub_datetime': tampered_creation_date,
            'edit_datetime': tampered_creation_date
        }

        resp = self.client.post(
            reverse('guides:create'), data=post_data, follow=True
        )
        created_guide = resp.context['object']
        self.assertEqual(created_guide.title, "test guide")
        self.assertEqual(created_guide.overview, "test guide overview")
        self.assertEqual(created_guide.content.raw, "test guide content")
        self.assertEqual(created_guide.author, self.user)
        self.assertNotEqual(created_guide.pub_datetime, tampered_creation_date)
        self.assertNotEqual(created_guide.edit_datetime, tampered_creation_date)
        self.assertNotEqual(created_guide.id, 41092)


class MemberUserCannotUpdateGuideDataTests(TestCase):
    """Ensure that a member cannot update excluded fields on a guide."""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user('testmember', password='testpass')
        cls.social_account = SocialAccount.objects.create(
            user=cls.user,
            uid=42,
            extra_data={'guild': {'id': '55555', 'permissions': 0x63584C0}}
        )
        cls.guide = Guide.objects.create(
            title="Test guide",
            overview="Test guide overview",
            content="Test guide content",
            author=cls.user
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_member_cannot_change_excluded_fields_on_update(self):
        """Ensures that the member cannot edit excluded fields when updating a guide."""

        tampered_edit_date = datetime.utcnow()
        data = {
            'id': 192031029321,
            'title': "random test guide",
            'overview': "another test overview",
            'content': "more test content",
            'author_id': 2941,
            'pub_datetime': tampered_edit_date,
            'edit_datetime': tampered_edit_date
        }

        resp = self.client.post(
            reverse('guides:edit', kwargs={'pk': self.guide.id}), data=data, follow=True
        )
        created_guide = resp.context['object']

        self.assertEqual(created_guide.title, data['title'])
        self.assertEqual(created_guide.overview, data['overview'])
        self.assertEqual(created_guide.content.raw, data['content'])
        self.assertEqual(created_guide.author, self.user)
        self.assertNotEqual(created_guide.pub_datetime, tampered_edit_date)
        self.assertNotEqual(created_guide.edit_datetime, tampered_edit_date)
        self.assertNotEqual(created_guide.id, 41092)
