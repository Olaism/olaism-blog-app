from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

from ..models import Post
from ..views import publish_post

User = get_user_model()

class LoginRequiredPostPublishViewTest(TestCase):

    def test_redirection(self):
        login_url = reverse('login')
        url = reverse('publish_post', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertRedirects(response, f"{login_url}?next={url}")

class PublishPostViewTest(TestCase):

    def setUp(self):
        author = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123456'
        )

        self.post = Post.objects.create(
            title = 'Test Post',
            author = author,
            body = 'Just a text',
        )

        self.client.login(username="testuser", password="testpassword123456")

        url = reverse('publish_post', kwargs={'pk': 1})

        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_resolve_url_to_correct_view(self):
        view = resolve('/posts/1/publish/')
        self.assertEquals(view.func, publish_post)

    def test_publish_post(self):
        self.assertTrue(self.post.status, 'published')

class UnPublishPostViewTest(TestCase):

    def setUp(self):
        author = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123456'
        )

        self.post = Post.objects.create(
            title = 'Test Post',
            author = author,
            body = 'Just a text',
            status = "published"
        )

        self.client.login(username="testuser", password="testpassword123456")

        url = reverse('publish_post', kwargs={'pk': 1})

        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_resolve_url_to_correct_view(self):
        view = resolve('/posts/1/publish/')
        self.assertEquals(view.func, publish_post)

    def test_publish_post(self):
        self.assertTrue(self.post.status, 'draft')