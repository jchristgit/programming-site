from django.contrib.auth.models import User
from django.test import TestCase, TransactionTestCase, override_settings
from django.urls import reverse

from .models import Guide
from .views import IndexView


INDEX_GUIDE_CONTEXT_NAME = IndexView.context_object_name


class NoGuidesTests(TestCase):
    """
    Scenario:
        Empty database, meaning:
        - No Guide is present
        - No User is present
    """

    def test_index_status_200(self):
        resp = self.client.get(reverse('guides:index'))
        self.assertEqual(resp.status_code, 200)

    def test_detail_status_404(self):
        resp = self.client.get(reverse('guides:detail', kwargs={'pk': 1}))
        self.assertEqual(resp.status_code, 404)

    def test_no_guides_passes_empty_context_data(self):
        """
        Since no Guides exist in the database,
        the index page should receive an empty query
        set for the `guides` context object.
        """

        resp = self.client.get(reverse('guides:index'))
        context_guides = resp.context[INDEX_GUIDE_CONTEXT_NAME]

        self.assertFalse(context_guides.exists())
        self.assertSequenceEqual(context_guides, [])


class AnonymousUserSingleGuideTests(TransactionTestCase):
    """
    Scenario:
        - 1 existing Guide
        - Anonymous User accesses the site
    """

    fixtures = ['anonymous_user_single_guide']

    def setUp(self):
        self.guide = Guide.objects.first()

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

    def test_anonymous_user_create_guide_status_403(self):
        """
        Anonymous Users should get 403 Forbidden
        when attempting to access the form used
        to create a guide.
        """

        resp = self.client.get(reverse('guides:create'))
        self.assertEqual(resp.status_code, 403)

    def test_anonymous_user_edit_guide_status_403(self):
        """
        Anonymous Users should get 403 Forbidden
        when attempting to access the form used
        to edit a guide.
        """

        resp = self.client.get(reverse('guides:edit', kwargs={'pk': self.guide.id}))
        self.assertEqual(resp.status_code, 403)

    def test_anonymous_user_delete_guide_status_403(self):
        """
        Anonymous Users should get 403 Forbidden
        when attempting to access the form
        used to delete a guide.
        """

        resp = self.client.get(reverse('guides:delete', kwargs={'pk': self.guide.id}))
        self.assertEqual(resp.status_code, 403)


class GuestUserSingleGuideTests(TransactionTestCase):
    """
    Scenario:
        - 1 existing Guide
        - Guest accesses the site
    """

    fixtures = ['guest_user_single_guide']

    def setUp(self):
        self.guide = Guide.objects.first()
        user = User.objects.filter(username='guesttestusername').first()
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

    def test_guest_user_create_guide_status_403(self):
        """
        Guest Users should get 403 Forbidden
        when attempting to access the form
        used to create a new guide.
        """

        resp = self.client.get(reverse('guides:create'))
        self.assertEqual(resp.status_code, 403)

    def test_guest_user_edit_guide_status_403(self):
        """
        Guest Users should get 403 Forbidden
        when attempting to access the form
        used to edit a Guide.
        """

        resp = self.client.get(reverse('guides:edit', kwargs={'pk': self.guide.id}))
        self.assertEqual(resp.status_code, 403)

    def test_guest_user_delete_guide_status_403(self):
        """
        Guest Users should get 403 Forbidden
        when attempting to access the form
        used to delete a Guide.
        """

        resp = self.client.get(reverse('guides:delete', kwargs={'pk': self.guide.id}))
        self.assertEqual(resp.status_code, 403)


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


class AuthorUserSingleGuideTests(TransactionTestCase):
    """
    Scenario:
        - 1 existing Guide
        - Author (also Member) of the Guide accesses the site
    """

    fixtures = ['author_user_single_guide']
    multi_db = True

    def setUp(self):
        self.guide = Guide.objects.filter(id=1).first()
        author = User.objects.filter(id=20).first()
        self.client.force_login(author)

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

        resp = self.client.get(reverse('guides:create'))
        self.assertEqual(resp.status_code, 200)

    @override_settings(DISCORD_GUILD_ID=42)
    def test_author_user_get_edit_guide_status_200(self):
        """
        The author should get 200 OK when attempting
        to GET `guides:edit` the guide that they created.
        """

        resp = self.client.get(reverse('guides:edit', kwargs={'pk': self.guide.id}))
        self.assertEqual(resp.status_code, 200)

    @override_settings(DISCORD_GUILD_ID=42)
    def test_member_user_get_delete_guide_status_200(self):
        """
        The author should get 200 OK when attempting
        to GET `guides:delete` for a guide they created.
        """

        resp = self.client.get(reverse('guides:delete', kwargs={'pk': self.guide.id}))
        self.assertEqual(resp.status_code, 200)


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
