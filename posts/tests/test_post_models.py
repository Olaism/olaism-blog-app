from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import Post

User = get_user_model()

class PostModelTest(TestCase):
    def setUp(self):
        author = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='test123456'
        )

        self.draft_status_post = Post.objects.create(
            title = 'Test Post',
            author = author,
            body = 'Just a text',
        )

        self.publish_status_post = Post.objects.create(
            title = 'Test Post 2',
            author = author,
            body = 'Just another text',
            status = 'publish'
        )

    def test_post_creation(self):
        self.assertTrue(Post.objects.exists())
        self.assertEqual(Post.objects.count(), 2)

    def test_draft_status_post(self):
        self.assertEqual(self.draft_status_post.title, 'Test Post')
        self.assertEqual(self.draft_status_post.author.username, 'testuser')
        self.assertEqual(self.draft_status_post.body, 'Just a text')
        self.assertEqual(self.draft_status_post.status, 'draft')

    def test_publish_status_post(self):
        self.assertEqual(self.publish_status_post.title, 'Test Post 2')
        self.assertEqual(self.publish_status_post.author.username, 'testuser')
        self.assertEqual(self.publish_status_post.body, 'Just another text')
        self.assertEqual(self.publish_status_post.status, 'publish')