from django.contrib.auth.models import User
from django.test import TransactionTestCase, override_settings
from django.urls import reverse

from guides.models import Guide

from . import INDEX_GUIDE_CONTEXT_NAME


class MemberUserSingleGuideTests(TransactionTestCase):
    """
    Scenario:
        - 1 existing Guide
        - Member accesses the site
    """

    fixtures = ['member_user_single_guide']
    multi_db = True

    def setUp(self):
        self.guide = Guide.objects.first()
        user = User.objects.filter(id=20).first()
        self.client.force_login(user)

    def test_index_status_200(self):
        resp = self.client.get(reverse('guides:index'))
        self.assertEqual(resp.status_code, 200)

    def test_detail_for_created_guide_status_200(self):
        resp = self.client.get(reverse('guides:detail', kwargs={'pk': self.guide.id}))
        self.assertEqual(resp.status_code, 200)

    def test_detail_for_unknown_guide_status_404(self):
        resp = self.client.get(reverse('guides:detail', kwargs={'pk': 2}))
        self.assertEqual(resp.status_code, 404)

    def test_index_context_is_only_created_guide(self):
        """
        A single guide was created, and no other
        data should appear within the guides
        context object on the index template.
        """

        resp = self.client.get(reverse('guides:index'))
        self.assertSequenceEqual(resp.context[INDEX_GUIDE_CONTEXT_NAME], [self.guide])

    def test_index_links_to_new_guide(self):
        """
        When a guide exists, the index page
        should include a link to it in its
        list of all guides.
        """

        resp = self.client.get(reverse('guides:index'))
        guide_link = reverse('guides:detail', kwargs={'pk': self.guide.id})
        self.assertIn(guide_link.encode('utf-8'), resp.content)

    @override_settings(DISCORD_GUILD_ID=42)
    def test_member_user_create_guide_status_200(self):
        """
        Members should be allowed to create a Guide,
        thus the edit form for creating a guide
        on `guides:create` should respond with 200 OK.
        """

        resp = self.client.get(reverse('guides:create'))
        self.assertEqual(resp.status_code, 200)

    @override_settings(DISCORD_GUILD_ID=42)
    def test_member_user_edit_guide_status_403(self):
        """
        Members should get 403 Forbidden when
        attempting to access the edit form to
        guides that they did not create.
        """

        resp = self.client.get(reverse('guides:edit', kwargs={'pk': self.guide.id}))
        self.assertEqual(resp.status_code, 403)

    @override_settings(DISCORD_GUILD_ID=42)
    def test_member_user_delete_guide_status_403(self):
        """
        Members should get 403 Forbidden when
        attempting to get the confirmation form
        to delete guides they did not create.
        """

        resp = self.client.get(reverse('guides:delete', kwargs={'pk': self.guide.id}))
        self.assertEqual(resp.status_code, 403)


class MemberUserGuideInteractionsTests(TransactionTestCase):
    """
    Scenario:
        - 1 existing Guide
        - Member accesses the site
        - Member uses guide creation, edit, and deletion views
    """

    fixtures = ['member_user_no_guide']
    multi_db = True

    @classmethod
    def setUpClass(cls):
        cls.guide_data = {
            'title': 'test guide',
            'overview': 'test guide overview',
            'content': 'test guide content'
        }
        edit_data = cls.guide_data.copy()
        edit_data['title'] = 'Edited test guide'
        cls.guide_data_edit = edit_data

    def setUp(self):
        self.user = User.objects.first()
        self.client.force_login(self.user)

    @override_settings(DISCORD_GUILD_ID=42)
    def test_member_user_can_create_guide(self):
        """
        A guild member should be able to create a Guide,
        and should get redirected to it after creation.
        """

        guide_create_post = self.client.post(reverse('guides:create'), data=self.guide_data)
        self.assertEqual(guide_create_post.status_code, 302)

        guide = Guide.objects.first()
        self.assertEqual(guide.title, self.guide_data['title'])
        self.assertEqual(guide.overview, self.guide_data['overview'])
        self.assertEqual(guide.content.raw, self.guide_data['content'])
        self.assertEqual(guide.author, self.user)

        self.assertIn(reverse('guides:detail', kwargs={'pk': guide.id}), guide_create_post.url)

    @override_settings(DISCORD_GUILD_ID=42)
    def test_member_user_can_edit_owned_guide(self):
        """
        A guild member should be able to
        edit a guide that they created,
        and saving the edit should redirect
        them to the detail view for the guide.
        """

        self.client.post(reverse('guides:create'), data=self.guide_data)
        guide = Guide.objects.first()
        guide_edit_get = self.client.get(reverse('guides:edit', kwargs={'pk': guide.id}))
        self.assertEqual(guide_edit_get.status_code, 200)

        guide_edit_post = self.client.post(reverse('guides:edit', kwargs={'pk': guide.id}), data=self.guide_data_edit)
        guide.refresh_from_db()
        self.assertEqual(guide_edit_post.status_code, 302)
        self.assertEqual(guide.title, self.guide_data_edit['title'])
        self.assertEqual(guide.overview, self.guide_data_edit['overview'])
        self.assertEqual(guide.content.raw, self.guide_data_edit['content'])
        self.assertEqual(guide.author, self.user)

        self.assertTrue(guide_edit_post.url.endswith(reverse('guides:detail', kwargs={'pk': guide.id})))

    @override_settings(DISCORD_GUILD_ID=42)
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

        self.client.post(reverse('guides:create'), data=self.guide_data)
        guide = Guide.objects.first()

        guide_delete_get = self.client.get(reverse('guides:delete', kwargs={'pk': guide.id}))
        self.assertEqual(guide_delete_get.status_code, 200)

        guide_delete_delete = self.client.delete(reverse('guides:delete', kwargs={'pk': guide.id}))
        self.assertEqual(guide_delete_delete.status_code, 302)
        self.assertTrue(guide_delete_delete.url.endswith(reverse('guides:index')))

        guide_detail_get = self.client.get(reverse('guides:detail', kwargs={'pk': guide.id}))
        self.assertEqual(guide_detail_get.status_code, 404)
