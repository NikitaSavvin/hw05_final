from django.test import TestCase
from django.urls import reverse


class TestAbout(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_about_author(self):
        response = self.client.get(reverse('about:author'))
        self.assertTemplateUsed(response, 'about/author.html')

    def test_tech_author(self):
        response = self.client.get(reverse('about:tech'))
        self.assertTemplateUsed(response, 'about/tech.html')
