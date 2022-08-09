from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

from ..models import Post
from ..views import PostListView

User = get_user_model()

class PostListViewTest(TestCase):

    def setUp(self):
        author = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123456'
        )

        post = Post.objects.create(
            title = 'Test Post',
            author = author,
            body = 'Just a text',
        )

        url = reverse('post_list')

        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_url_resolve_correct_to_view(self):
        view = resolve('/posts/')
        self.assertEqual(view.func.view_class, PostListView)

    def test_html_template_used(self):
        self.assertTemplateUsed(self.response, 'blog/post_list.html')

    def test_have_links(self):
        pass

    def test_does_not_have_links(self):
        pass