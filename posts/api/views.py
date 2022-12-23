from rest_framework import generics

from posts.models import Post
from .serializers import (
    PostListSerializer,
    PostDetailSerializer,
    PostCreateSerializer
)

class PostListAPIView(generics.ListAPIView):
    queryset = Post.published.all()
    serializer_class = PostListSerializer


class PostCreateAPIView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer


class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.published.all()
    serializer_class = PostDetailSerializer
    lookup_field = "slug"