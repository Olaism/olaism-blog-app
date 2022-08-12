from django.test import TestCase
from django.forms import ModelForm
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

from ..models import Post
from ..views import PostCreateView

class PostCreateTestCase(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="testuser@gmail.com",
            password="testpassword123456"
        )
        self.url = reverse('post_create')

class LoginRequiredPostCreateViewTests(PostCreateTestCase):

    def test_redirection(self):
        response = self.client.get(self.url)
        login_url = reverse('login')
        self.assertRedirects(response, f"{login_url}?next={self.url}")

class PostCreateViewTests(PostCreateTestCase):

    def setUp(self):
        super().setUp()
        self.client.login(
            username="testuser",
            password="testpassword123456"
        )
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_url_resolves_to_correct_view(self):
        view = resolve('/posts/new/')
        self.assertEquals(view.func.view_class, PostCreateView)

    def test_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, 'blog/post_create.html')

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_form_class(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, ModelForm)

    def test_form_inputs(self):
        self.assertContains(self.response, "<input", 3)
        self.assertContains(self.response, "<textarea", 1)
        self.assertContains(self.response, 'Create new post</button>', 1)

class SuccessfulPostCreateViewTests(PostCreateTestCase):

    def setUp(self):
        super().setUp()
        self.client.login(username="testuser", password="testpassword123456")
        self.response = self.client.post(self.url, {
            'title': 'My Post',
            'body': "This is the body",
            'status': "draft"
        })

    def test_redirection(self):
        post_url = reverse('post_detail', kwargs={'pk': 1})
        self.assertRedirects(self.response, post_url)

    def test_post_creation(self):
        self.assertTrue(Post.objects.exists())


class InvalidPostCreateViewTests(PostCreateTestCase):

    def setUp(self):
        super().setUp()
        self.client.login(username="testuser", password="testpassword123456")
        self.response = self.client.post(self.url, {})

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_post_creation(self):
        self.assertFalse(Post.objects.exists())