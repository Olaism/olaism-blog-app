from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.http import Http404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    DetailView,
    ListView,
)

from django.views.generic.edit import (
    CreateView,
    DeleteView,
    UpdateView,
)
from taggit.models import Tag

from .models import Post
from .forms import EmailPostForm


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, *args, **kwargs):
        post = self.get_object()
        context = super().get_context_data(*args, **kwargs)
        post.views += 1
        post_tags_ids = post.tags.values_list('id', flat=True)
        similar_posts = Post.objects.filter(draft=False).filter(
            tags__in=post_tags_ids).exclude(id=post.id)
        context['similar_posts'] = similar_posts.annotate(
            same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
        return context

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not self.request.user.is_anonymous:
            if obj.draft and obj.author != self.request.user:
                raise Http404
        else:
            if obj.status == 'draft':
                raise Http404
        return super().dispatch(request, *args, **kwargs)


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
            raise Http404
        return super().dispatch(request, *args, **kwargs)


@method_decorator(login_required, name="dispatch")
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('my_posts')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise Http404
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
        raise Http404
    return render(request, 'blog/my_posts.html', {'posts': posts})
