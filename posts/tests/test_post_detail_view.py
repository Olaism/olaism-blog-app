from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

from ..models import Post
from ..views import PostDetailView

User = get_user_model()

class PostDetailViewTestCase(TestCase):

    def setUp(self):
        self.author = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123456'
        )

        self.author2 = User.objects.create_user(
            username='testuser2',
            email='testuser2@example.com',
            password='testpassword789234'
        )

        self.draft_post = Post.objects.create(
            title = 'Test Post',
            author = self.author,
            body = 'Just a draft text',
        )

        self.published_post = Post.objects.create(
            title = 'Test Post 2',
            author = self.author,
            body = 'Just a published text',
            status = 'published',
        )

class AnonymousDraftPostDetailView(PostDetailViewTestCase):

    def setUp(self):
        super().setUp()
        url = self.draft_post.get_absolute_url()
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 403)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, '403.html')

class UnauthorizedUserDraftDetailView(PostDetailViewTestCase):

    def setUp(self):
        super().setUp()
        url = self.draft_post.get_absolute_url()
        self.client.login(username='testuser2', password='testpassword789234')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 403)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, '403.html')

class DraftPostDetailView(PostDetailViewTestCase):

    def setUp(self):
        super().setUp()
        self.url = self.draft_post.get_absolute_url()
        self.client.login(username='testuser', password='testpassword123456')
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_url_resolve_correct_to_view(self):
        view = resolve(self.url)
        self.assertEqual(view.func.view_class, PostDetailView)

    def test_html_template_used(self):
        self.assertTemplateUsed(self.response, '_base.html')
        self.assertTemplateUsed(self.response, 'blog/post_detail.html')