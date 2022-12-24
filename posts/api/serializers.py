from django.contrib.auth import get_user_model

from rest_framework import serializers
from taggit.serializers import (
    TagListSerializerField,
    TaggitSerializer
)
from posts.models import Post


class AuthorSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'last_login', 'is_staff', 'posts')

    def get_posts(self, obj):
        return Post.objects.filter(author=obj).count()

class PostCreateSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    class Meta:
        model = Post
        fields = ('title', 'highlight', 'image_url', 'author', 'body', 'featured', 'read_time', 
        'tags', 'publish')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetailSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    author = AuthorSerializer(read_only=True)
    class Meta:
        model = Post
        lookup_field = 'slug'
        fields = ('id', 'title', 'highlight', 'author', 'image_url', 'publish', 'updated', 'body', 
        'tags', 'draft', 'featured', 'read_time', 'tags')

class PostListSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    author = serializers.StringRelatedField()
    class Meta:
        model = Post
        lookup_field = 'slug'
        fields = ('id', 'title', 'url', 'author')