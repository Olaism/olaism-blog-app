from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

from ..models import Post
from ..views import status_change

User = get_user_model()

class LoginRequiredStatusChangeViewTest(TestCase):

    def test_redirection(self):
        login_url = reverse('login')
        url = reverse('status_change', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertRedirects(response, f"{login_url}?next={url}")

class StatusChangeViewTestCase(TestCase):

    def setUp(self):
        author = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123456'
        )
        unauthorized_user = User.objects.create_user(
            username='testuser2',
            email = 'testuser2@example.com',
            password = 'testpassword456123'
        )
        self.post = Post.objects.create(
            title = 'Test Post',
            author = author,
            body = 'Just a text',
            tags = 'test, testing'
        )
        self.url = reverse('status_change', kwargs={'pk': self.post.pk})

class UnauthorizedStatusChangeViewTest(StatusChangeViewTestCase):

    def setUp(self):
        super().setUp()
        self.client.login(username="testuser2", password="testpassword456123")
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 403)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, '403.html')

class AuthorizedStatusChangeViewTest(StatusChangeViewTestCase):

    def setUp(self):
        super().setUp()
        self.client.login(
            username='testuser',
            password='testpassword123456',
        )
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_resolve_url_to_correct_view(self):
        view = resolve('/posts/1/status-change/')
        self.assertEquals(view.func, status_change)

    def test_publish_post(self):
        self.assertTrue(self.post.status, 'published')

    def test_reverse_status_change(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(self.post.status, 'draft')