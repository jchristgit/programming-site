from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.test import TestCase
from django.urls import reverse


class AnonymousUserHomeAppTests(TestCase):
    def test_index_status_200(self):
        self.assertEqual(self.client.get(reverse('home:index')).status_code, 200)

    def test_context_user_attributes_properly_set(self):
        res = self.client.get(reverse('home:index'))
        user = res.context['user']

        self.assertTrue(user.is_anonymous)
        self.assertFalse(user.is_authenticated)
        self.assertFalse(user.is_member)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)


class AnonymousUserWithMemberInDatabaseHomeAppTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        set_up_oauth_test_data(cls, [{
            'id': '181866934353133570',
            'permissions': 0x63584c0
        }])

    def test_index_status_200(self):
        self.assertEqual(self.client.get(reverse('home:index')).status_code, 200)

    def test_created_user_attributes_properly_set(self):
        self.assertTrue(self.user.is_anonymous)
        self.assertFalse(self.user.is_authenticated)
        self.assertFalse(self.user.is_member)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_context_user_attributes_properly_set(self):
        res = self.client.get(reverse('home:index'))
        user = res.context['user']

        self.assertTrue(user.is_anonymous)
        self.assertFalse(user.is_authenticated)
        self.assertFalse(user.is_member)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)


class AuthenticatedUserHomeAppTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        set_up_oauth_test_data(cls, [])

    def setUp(self):
        self.client.force_login(self.user)

    def test_index_status_200(self):
        self.assertEqual(self.client.get(reverse('home:index')).status_code, 200)

    def test_created_user_attributes_properly_set(self):
        self.assertFalse(self.user.is_anonymous)
        self.assertTrue(self.user.is_authenticated)
        self.assertFalse(self.user.is_member)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_context_user_attributes_properly_set(self):
        res = self.client.get(reverse('home:index'))
        user = res.context['user']

        self.assertFalse(user.is_anonymous)
        self.assertTrue(user.is_authenticated)
        self.assertFalse(user.is_member)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)


class GuestUserHomeAppTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        set_up_oauth_test_data(cls, [{
            'id': '181866934353133570',
            'permissions': 0x140800
        }])

    def setUp(self):
        self.client.force_login(self.user)

    def test_index_status_200(self):
        self.assertEqual(self.client.get(reverse('home:index')).status_code, 200)

    def test_created_user_attributes_properly_set(self):
        self.assertFalse(self.user.is_anonymous)
        self.assertTrue(self.user.is_authenticated)
        self.assertFalse(self.user.is_member)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_context_user_attributes_properly_set(self):
        res = self.client.get(reverse('home:index'))
        user = res.context['user']

        self.assertFalse(user.is_anonymous)
        self.assertTrue(user.is_authenticated)
        self.assertFalse(user.is_member)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)


class MemberUserHomeAppTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        set_up_oauth_test_data(cls, [{
            'id': '181866934353133570',
            'permissions': 0x63584c0
        }])

    def setUp(self):
        self.client.force_login(self.user)

    def test_index_status_200(self):
        self.assertEqual(self.client.get(reverse('home:index')).status_code, 200)

    def test_created_user_attributes_properly_set(self):
        self.assertFalse(self.user.is_anonymous)
        self.assertTrue(self.user.is_authenticated)
        self.assertTrue(self.user.is_member)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_context_user_attributes_properly_set(self):
        res = self.client.get(reverse('home:index'))
        user = res.context['user']

        self.assertFalse(user.is_anonymous)
        self.assertTrue(user.is_authenticated)
        self.assertTrue(user.is_member)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)


class StaffUserHomeAppTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        set_up_oauth_test_data(cls, [{
            'id': '181866934353133570',
            'permissions': 0x8
        }])

    def setUp(self):
        self.client.force_login(self.user)

    def test_index_status_200(self):
        self.assertEqual(self.client.get(reverse('home:index')).status_code, 200)

    def test_created_user_attributes_properly_set(self):
        self.assertFalse(self.user.is_anonymous)
        self.assertTrue(self.user.is_authenticated)
        self.assertTrue(self.user.is_member)
        self.assertTrue(self.user.is_staff)
        self.assertTrue(self.user.is_superuser)

    def test_context_user_attributes_properly_set(self):
        res = self.client.get(reverse('home:index'))
        user = res.context['user']

        self.assertFalse(user.is_anonymous)
        self.assertTrue(user.is_authenticated)
        self.assertTrue(user.is_member)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)


def set_up_oauth_test_data(cls, guilds):
    cls.current_site = Site.objects.get_current()
    cls.discord = cls.current_site.socialapp_set.create(
        provider="discord",
        name="discord",
        client_id="1234567890",
        secret="0987654321",
    )
    cls.user = get_user_model()(
        username="test", email="test@test.com", password="testpassword", discriminator=0000
    )
    cls.user.save()
    social_account = SocialAccount.objects.create(
        user=cls.user, provider=cls.discord, uid=cls.user.id
    )
    adapter = DefaultSocialAccountAdapter()
    cls.social_account = adapter.populate_user(None, social_account, {
        'username': 'test user social account name',
        'discriminator': '0000',
        'guilds': guilds
    })
