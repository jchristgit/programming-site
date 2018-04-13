from django.contrib.auth.models import User
from django.test import TransactionTestCase, override_settings
from django.urls import reverse

from guides.models import Guide

from . import INDEX_GUIDE_CONTEXT_NAME


class AdminUserUnownedGuideInteractionsTests(TransactionTestCase):
    """
    Scenario:
        - 1 existing Guide
        - (Discord) administrator accesses the site
        - (Discord) administrator uses guide creation, edit, and delete views
          for guides not owned by them
    """

    fixtures = ['admin_user_unowned_guide']
    multi_db = True

    def setUp(self):
        user = User.objects.filter(username="admintestuser").first()
        self.client.force_login(user)

    @override_settings(
        DISCORD_GUILD_ID=42,
        DISCORD_ADMIN_ROLE_ID=10
    )
    def test_staff_can_edit_unowned_guide(self):
        """
        A staff member should be able to edit
        a guide that they do not own, and
        editing the guide should redirect them
        towards the detail page for it.
        """

        guide = Guide.objects.first()
        edit_data = {
            'title': 'edited title',
            'overview': 'edited overview',
            'content': 'edited content'
        }
        guide_edit_post = self.client.post(reverse('guides:edit', kwargs={'pk': guide.id}), data=edit_data)
        guide.refresh_from_db()

        guide_edit_get = self.client.get(reverse('guides:edit', kwargs={'pk': guide.id}))
        self.assertEqual(guide_edit_get.status_code, 200)

        self.assertEqual(guide_edit_post.status_code, 302)
        self.assertEqual(guide.title, edit_data['title'])
        self.assertEqual(guide.overview, edit_data['overview'])
        self.assertEqual(guide.content.raw, edit_data['content'])
        self.assertTrue(guide_edit_post.url.endswith(reverse('guides:detail', kwargs={'pk': guide.id})))

        guide_detail = self.client.get(reverse('guides:detail', kwargs={'pk': guide.id}))
        self.assertEqual(guide_detail.context['guide'], guide)

    @override_settings(
        DISCORD_GUILD_ID=42,
        DISCORD_ADMIN_ROLE_ID=10
    )
    def test_staff_can_delete_unowned_guide(self):
        """
        A staff member should be able to delete
        a guide that they do not own, and
        deleting the guide should redirect them
        towards `guides:index`.
        """

        guide = Guide.objects.first()
        guide_delete_get = self.client.get(reverse('guides:delete', kwargs={'pk': guide.id}))
        self.assertEqual(guide_delete_get.status_code, 200)

        guide_delete_delete = self.client.delete(reverse('guides:delete', kwargs={'pk': guide.id}))
        self.assertEqual(guide_delete_delete.status_code, 302)
        self.assertIsNone(Guide.objects.first())
        self.assertTrue(guide_delete_delete.url.endswith(reverse('guides:index')))

        guide_index = self.client.get(reverse('guides:index'))
        self.assertSequenceEqual(guide_index.context[INDEX_GUIDE_CONTEXT_NAME], [])
