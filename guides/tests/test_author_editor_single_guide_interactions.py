from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import override_settings, TestCase

from guides.models import Guide


class AuthorAndEditorSingleGuideInteractionTests(TestCase):
    """
    Scenario:
        - Author creates a guide
        - Editor interacts with the edit and delete views
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
        self.edit_guide_data = {
            'title': 'new guide title',
            'overview': 'new guide overview',
            'content': 'new guide content'
        }

        self.client.force_login(self.editor)

    @override_settings(DISCORD_GUILD_ID=42)
    def test_editor_can_edit_guide(self):
        """Editors should be able to access the `guides:edit` view."""

        resp = self.client.post(reverse('guides:edit', kwargs={'pk': self.guide.id}), data=self.edit_guide_data)
        self.guide.refresh_from_db()

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(self.guide.title, self.edit_guide_data['title'])
        self.assertEqual(self.guide.overview, self.edit_guide_data['overview'])
        self.assertEqual(self.guide.content.raw, self.edit_guide_data['content'])
        self.assertEqual(self.guide.author, self.author)
        self.assertSequenceEqual(self.guide.editors.all(), [self.editor])

        self.assertTrue(resp.url.endswith(reverse('guides:detail', kwargs={'pk': self.guide.id})))

    @override_settings(DISCORD_GUILD_ID=42)
    def test_editor_cannot_change_guide_editors(self):
        """Editors should not be able to mess with the `editors` of a Guide."""

        malicious_guide_data = {
            **self.edit_guide_data,
            'editors': [self.author.id, self.editor.id]
        }

        resp = self.client.post(reverse('guides:edit', kwargs={'pk': self.guide.id}), data=malicious_guide_data)
        self.guide.refresh_from_db()

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(self.guide.title, self.edit_guide_data['title'])
        self.assertEqual(self.guide.overview, self.edit_guide_data['overview'])
        self.assertEqual(self.guide.content.raw, self.edit_guide_data['content'])
        self.assertEqual(self.guide.author, self.author)
        self.assertSequenceEqual(self.guide.editors.all(), [self.editor])

        self.assertTrue(resp.url.endswith(reverse('guides:detail', kwargs={'pk': self.guide.id})))

    @override_settings(DISCORD_GUILD_ID=42)
    def test_editor_cannot_delete_guide(self):
        """Editors should not be able to access the `guides:delete` view."""

        resp = self.client.post(reverse('guides:delete', kwargs={'pk': self.guide.id}))
        self.assertEqual(resp.status_code, 403)
