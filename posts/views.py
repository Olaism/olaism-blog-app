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

from .models import Post
from .forms import EmailPostForm

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        return Post.objects.filter(status='published')

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

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
    fields = ('title', 'body', 'status',)
    # success_url = reverse_lazy()
    template_name = 'blog/post_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

@method_decorator(login_required, name="dispatch")
class PostUpdateView(UpdateView):
    model = Post
    fields = ('title', 'body',)
    # success_url = reverse_lazy()
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
    success_url = reverse_lazy('post_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

@login_required
def publish_post(request, pk):
    posts = Post.objects.filter(author=request.user)
    post = get_object_or_404(Post, pk=pk)
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