from django.test import TestCase
from django.urls import reverse


class HomeAppTests(TestCase):
    def test_index_status_200(self):
        assert self.client.get(reverse('home:index')).status_code == 200
