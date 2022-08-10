from django.shortcuts import render
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    DetailView,
    DeleteView,
)

from django.views.generic.edit import (
    CreateView,
    UpdateView
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
    fields = ('title', 'body', 'status',)
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

def post_share(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk, status='published')

    if request.method == 'POST':
        form = EmailPostForm()
        if form.is_valid():
            cd = form.cleaned_data
            # send email
    else:
        form = EmailPostForm()

    return render(request, 'blog/post_share.html', {'post': post, 'form': form})
