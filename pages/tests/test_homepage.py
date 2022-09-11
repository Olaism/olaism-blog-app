from django.test import TestCase
from django.urls import reverse, resolve

from ..views import HomePageView

class HomePageTests(TestCase):

    def setUp(self):
        url = reverse('home')
        self.response = self.client.get(url)

    def test_homepage_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_homepage_url_name(self):
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_resolve_url(self):
        view = resolve('/')
        self.assertEqual(view.func.view_class, HomePageView)

    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, '_base.html')
        self.assertTemplateUsed(self.response, 'pages/home.html')
        self.assertTemplateUsed(self.response, 'includes/post_list.html')
        self.assertTemplateUsed(self.response, 'includes/pagination.html')