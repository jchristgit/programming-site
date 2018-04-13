from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import override_settings, TestCase

from guides.models import Guide


class AuthorAndEditorSingleGuideTests(TestCase):
    """
    Scenario:
        - Author creates a guide
        - Editor uses the edit and delete views
    """

    fixtures = ['two_members_single_guide']

    def setUp(self):
        # TODO: If someone knows how to specify many-to-many relationships
        #       in the fixture, please move this to the fixture, thank you!

        self.author = User.objects.get(username='authorusername')
        self.editor = User.objects.get(username='editorusername')
        self.guide = Guide.objects.first()
        self.guide.editors.add(self.editor)
        self.guide.save()

        self.client.force_login(self.editor)

    def test_detail_status_200(self):
        resp = self.client.get(reverse('guides:detail', kwargs={'pk': self.guide.id}))
        self.assertEqual(resp.status_code, 200)

    @override_settings(DISCORD_GUILD_ID=42)
    def test_edit_status_200(self):
        """Editors should be able to access the `guides:edit` view."""

        resp = self.client.get(reverse('guides:edit', kwargs={'pk': self.guide.id}))
        self.assertEqual(resp.status_code, 200)

    @override_settings(DISCORD_GUILD_ID=42)
    def test_delete_status_403(self):
        """Editors should not be able to access the `guides:delete` view."""

        resp = self.client.get(reverse('guides:delete', kwargs={'pk': self.guide.id}))
        self.assertEqual(resp.status_code, 403)
