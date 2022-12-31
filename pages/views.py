from django.db.models import Q
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import (
    FormView,
    ListView,
    TemplateView,
)
from taggit.models import Tag

from posts.models import Post
from .forms import ContactForm


class HomePageView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['posts'] = Post.published.all()
        context['featured'] = Post.objects.filter(featured=True).first()
        return context


class PostListView(ListView):
    model = Post
    template_name = 'pages/posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self, **kwargs):
        tag_slug = self.kwargs.get('tag_slug') or None
        search_term = self.kwargs.get('search_term') or None
        posts = Post.published.all()
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            posts = posts.filter(tags__in=[tag])
        elif search_term:
            posts = posts.filter(
                Q(title__icontains=search_term) | Q(
                    author__username__icontains=search_term)
            )
        return posts

    def get_context_data(self, *args, **kwargs):
        tag_slug = self.kwargs.get('tag_slug') or None
        search_term = self.kwargs.get('search_term') or None
        context = super().get_context_data(*args, **kwargs)
        if tag_slug:
            context['tag'] = tag_slug
        elif search_term:
            context['query'] = search_term
        return context

class ContactPageView(FormView):
    template_name = 'pages/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact_success')

    def form_valid(self, form):
        form.send()
        return super().form_valid(form)


class ContactSuccessView(TemplateView):
    template_name = 'pages/contact_success.html'
