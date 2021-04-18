# using Python 3.8.5
from django.test import TestCase
from django.urls import reverse

class AboutView(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()


    def test_AboutView_url_exists_at_desired_location(self):
        url = reverse('about')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code,200)


# Create your tests here.
