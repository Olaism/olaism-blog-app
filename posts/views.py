from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    DetailView,
)

from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView,
)
from taggit.models import Tag

from .models import Post
from .forms import EmailPostForm

class PostListView(ListView):
    model = Post
    template_name = 'blog/posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        tag_slug = self.request.GET.get('tag')
        posts = Post.published.all()
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            posts = posts.filter(tags__in=[tag])
        return posts

    def get_context_data(self, *args, **kwargs):
        tag = self.request.GET.get('tag')
        context = super().get_context_data(*args, **kwargs)
        if tag:
            context['tag'] = tag
        context['admin_posts'] = Post.published.filter(author__is_staff=True)
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, *args, **kwargs):
        post = self.get_object()
        context = super().get_context_data(*args, **kwargs)
        post_tags_ids = post.tags.values_list('id', flat=True)
        similar_posts = Post.objects.filter(status='published').filter(tags__in=post_tags_ids).exclude(id=post.id)
        context['similar_posts'] = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
        return context

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not self.request.user.is_anonymous:
            if obj.status != 'published' and obj.author != self.request.user:
                raise PermissionDenied
        else:
            if obj.status == 'draft':
                raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
        

class PostSearchView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/post_search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        published_posts = Post.published.all()
        if query:
            return published_posts.filter(
                Q(title__icontains=query) | Q(author__username__icontains=query)
            )
        else:
            return []

    def get_context_data(self, *args, **kwargs):
        q = self.request.GET.get('q')
        context = super().get_context_data(*args, **kwargs)
        if not q:
            context["query"] = ''
        else:
            context["query"] = self.request.GET.get('q')
        return context

@method_decorator(login_required, name="dispatch")
class MyPostsView(ListView):
    model = Post
    template_name = 'blog/my_posts.html'
    context_object_name = 'posts'
    paginate_by = 20

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

@method_decorator(login_required, name="dispatch")
class PostCreateView(CreateView):
    model = Post
    fields = ('title', 'highlight', 'body', 'image_url', 'status', 'tags',)
    # success_url = reverse_lazy()
    template_name = 'blog/post_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

@method_decorator(login_required, name="dispatch")
class PostUpdateView(UpdateView):
    model = Post
    fields = ('title', 'highlight', 'body', 'image_url', 'tags',)
    success_url = reverse_lazy('my_posts')
    template_name = 'blog/post_update.html'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

@method_decorator(login_required, name="dispatch")
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('my_posts')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

@login_required
def status_change(request, slug):
    posts = Post.objects.filter(author=request.user)
    post = get_object_or_404(Post, slug=slug)
    if post.author == request.user:
        if post.status == 'draft':
            post.status = 'published'
            post.save()
        else:
            post.status = 'draft'
            post.save()
    else:
        raise PermissionDenied
    return render(request, 'blog/my_posts.html', {'posts': posts})