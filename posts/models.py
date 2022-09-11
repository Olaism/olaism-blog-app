from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.html import mark_safe
from django.contrib.auth import get_user_model

from markdown import markdown
from taggit.managers import TaggableManager

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=125)
    highlight = models.CharField(max_length=255, default="", blank=True)
    author = models.ForeignKey(
        get_user_model(), 
        on_delete = models.CASCADE,
        related_name = 'posts'
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES,
        default='draft'
    )
    featured = models.BooleanField(default=False)
    tags = TaggableManager()
    slug = models.SlugField(
        max_length=255, 
        blank=True, 
        null= True
    )

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})
        
    def get_body_as_markdown(self):
        return mark_safe(markdown(self.body, safe_mode='escape'))