from rest_framework import generics
from rest_framework import filters

from posts.models import Post
from posts.api.filters import (
    TagFieldFilter,
    DaysFieldFilter
)
from .serializers import (
    PostListSerializer,
    PostDetailSerializer,
    PostCreateSerializer
)


class PostListAPIView(generics.ListAPIView):
    queryset = Post.published.all()
    serializer_class = PostListSerializer
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter, TagFieldFilter, DaysFieldFilter]
    search_fields = ['title', 'author__username']
    ordering_fields = ['publish', 'read_time', 'views']
    ordering = ['publish']


class PostCreateAPIView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer


class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = "slug"
