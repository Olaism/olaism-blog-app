from django.test import TestCase
from django.forms import ModelForm
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

from ..models import Post
from ..views import PostDeleteView

class PostDeleteTestCase(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="testuser@gmail.com",
            password="testpassword123456"
        )
        self.post = Post.objects.create(
            title="My Post",
            body="This is the body of my post",
            author=self.user
        )
        self.url = reverse('post_delete', kwargs={'pk': 1})

class LoginRequiredPostDeleteViewTests(PostDeleteTestCase):

    def test_redirection(self):
        response = self.client.get(self.url)
        login_url=reverse("login")
        self.assertRedirects(response, f"{login_url}?next={self.url}")

class PostDeleteViewTests(PostDeleteTestCase):

    def setUp(self):
        super().setUp()
        self.client.login(
            username="testuser",
            password="testpassword123456"
        )
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_resolve_correct_url(self):
        view = resolve('/posts/1/delete/')
        self.assertEquals(view.func.view_class, PostDeleteView)

    def test_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, 'blog/post_delete.html')

    def test_csrf_protection(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_warning_message(self):
        warning_text = "Are you sure you want to delete this post?"
        self.assertContains(self.response, warning_text)

    def test_delete_button(self):
        self.assertContains(self.response, 'Yes, delete my post</button>', 1)


class SuccessfulPostDeleteViewTests(PostDeleteTestCase):

    def setUp(self):
        super().setUp()
        self.client.login(username="testuser", password="testpassword123456")
        self.response = self.client.post(self.url)

    def test_redirection(self):
        post_list_url = reverse('post_list')
        self.assertRedirects(self.response, post_list_url)

    def test_post_deletion(self):
        self.assertFalse(Post.objects.exists())