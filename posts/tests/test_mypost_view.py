from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

from ..models import Post
from ..views import MyPostsView

User = get_user_model()

class LoginRequiredMyPostsViewTest(TestCase):

    def test_redirection(self):
        login_url = reverse('login')
        url = reverse('my_posts')
        response = self.client.get(url)
        self.assertRedirects(response, f'{login_url}?next={url}')

class MyPostViewTestCase(TestCase):

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

        author1_post = Post.objects.bulk_create([
            Post(title="My Post 1", body='Body of my post 1', author=author1, status="published"),
            Post(title="My Post 2", body='Body of my post 2', author=author1),
            Post(title="My Post 3", body='Body of my post 3', author=author1),
            Post(title="My Post 4", body='Body of my post 4', author=author1),
            Post(title="My Post 5", body='Body of my post 5', author=author1, status="published"),
            Post(title="My Post 6", body='Body of my post 6', author=author1, status="published"),
        ])

        author2_post = Post.objects.bulk_create([
            Post(title="My Post 7", body='Body of my post 1', author=author2),
            Post(title="My Post 8", body='Body of my post 2', author=author2, status="published"),
        ])

        self.url = reverse('my_posts')

class LoginRequiredMyPostsViewTest(TestCase):

    def test_redirection(self):
        url = reverse('my_posts')
        response = self.client.get(url)
        self.assertRedirects(response, f'{reverse("login")}?next={url}')

class MyPostsViewTest(MyPostViewTestCase):
    
    def setUp(self):
        super().setUp()
        self.client.login(username="testuser", password="testpassword123456")
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_url_resolves_to_correct_view(self):
        view = resolve('/posts/my-post/')
        self.assertEquals(view.func.view_class, MyPostsView)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, 'blog/my_posts.html')

class Author1PostsViewTest(MyPostViewTestCase):

    def setUp(self):
        super().setUp()
        self.client.login(username="testuser", password="testpassword123456")
        self.response = self.client.get(self.url)

    def test_number_of_posts(self):
        posts = self.response.context.get('posts')
        self.assertEquals(len(posts), 6)

    def test_publish_buttons(self):
        self.assertContains(self.response, 'Publish', 3)

    def test_unpublish_buttons(self):
        self.assertContains(self.response, 'Unpublish', 3)

    def test_update_buttons(self):
        self.assertContains(self.response, 'Edit</a>', 6)

    def test_delete_buttons(self):
        self.assertContains(self.response, 'Delete</a>', 6)