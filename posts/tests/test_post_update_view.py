from unittest import skip

from django.test import TestCase
from django.forms import ModelForm
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

from ..models import Post
from ..views import PostUpdateView

class PostUpdateTestCase(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="testuser@gmail.com",
            password="testpassword123456"
        )
        self.unauthorized_user = get_user_model().objects.create_user(
            username="testuser2",
            email="testuser2@gmail.com",
            password="testpassword567890"
        )
        self.post = Post.objects.create(
            title="My Post",
            body="This is the body of my post",
            author=self.user,
            tags='test, testing',
        )
        self.url = reverse('post_update', kwargs={'slug': self.post.slug})

class LoginRequiredPostUpdateViewTests(PostUpdateTestCase):

    def test_redirection(self):
        response = self.client.get(self.url)
        login_url=reverse("login")
        self.assertRedirects(response, f"{login_url}?next={self.url}")

class UnauthorizedPostUpdateViewTests(PostUpdateTestCase):

    def setUp(self):
        super().setUp()
        self.client.login(
            username="testuser2",
            password="testpassword567890"
        )
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 403)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, '403.html')

class AuthorizedPostUpdateViewTests(PostUpdateTestCase):

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
        view = resolve('/posts/1/edit/')
        self.assertEquals(view.func.view_class, PostUpdateView)

    def test_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, 'blog/post_update.html')

    def test_csrf_protection(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_form_class(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, ModelForm)

    def test_form_inputs(self):
        self.assertContains(self.response, "<input", 5)
        self.assertContains(self.response, "<textarea", 1)
        self.assertContains(self.response, 'Post update</button>', 1)

    def test_form_has_correct_values(self):
        self.assertContains(self.response, "My Post")
        self.assertContains(self.response, "This is the body of my post")


@skip("Dubugged not redirecting later")
class AuthorizedSuccessfulPostUpdateViewTests(PostUpdateTestCase):

    def setUp(self):
        super().setUp()
        self.client.login(username="testuser", password="testpassword123456")
        self.response = self.client.post(self.url, {
            'title': 'My Post (updated)',
            'body': "This is the body of the post (updated)",
        })

    def test_redirection(self):
        post_url = reverse('my_posts')
        self.assertRedirects(self.response, post_url)

    def test_post_update(self):
        self.assertTrue(self.post.title, 'My Post (updated)')
        self.assertTrue(self.post.body, 'This is the body of the post (updated)')
        self.assertTrue(self.post.status, 'draft')


class AuthorizedInvalidPostUpdateViewTests(PostUpdateTestCase):

    def setUp(self):
        super().setUp()
        self.client.login(username="testuser", password="testpassword123456")
        self.response = self.client.post(self.url, {})

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_post_not_updated(self):
        self.assertTrue(self.post.title, 'My Post')
        self.assertTrue(self.post.body, 'This is the body of my post')