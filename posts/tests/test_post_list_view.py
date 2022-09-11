from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

from ..models import Post
from ..views import PostListView

User = get_user_model()

class PostListViewTest(TestCase):

    def setUp(self):
        author1 = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123456'
        )

        author2 = User.objects.create_user(
            username='testuser02',
            email='testuser02@example.com',
            password='testpassword021234'
        )

        post = Post.objects.bulk_create([
            Post(title="My Post 1", body='Body of my post 1', author=author1, status="published"),
            Post(title="My Post 2", body='Body of my post 2', author=author1),
            Post(title="My Post 3", body='Body of my post 3', author=author1),
            Post(title="My Post 4", body='Body of my post 4', author=author1),
            Post(title="My Post 5", body='Body of my post 5', author=author1, status="published"),
            Post(title="My Post 6", body='Body of my post 6', author=author1, status="published"),
        ])

        author2_post = Post.objects.bulk_create([
            Post(title="My Post 1", body='Body of my post 1', author=author2),
            Post(title="My Post 2", body='Body of my post 2', author=author2, status="published"),
        ])

        url = reverse('post_list')

        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_url_resolve_correct_to_view(self):
        view = resolve('/posts/')
        self.assertEqual(view.func.view_class, PostListView)

    def test_html_template_used(self):
        self.assertTemplateUsed(self.response, '_base.html')
        self.assertTemplateUsed(self.response, 'blog/posts.html')
        self.assertTemplateUsed(self.response, 'includes/pagination.html')

    def test_only_published_posts_in_list(self):
        posts = self.response.context.get('posts')
        self.assertEquals(len(posts), 4)