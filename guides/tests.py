from django.test import TestCase
from django.urls import reverse


class GuidesAppTests(TestCase):
    def test_index_status_200(self):
        assert self.client.get(reverse('guides:index')).status_code == 200
