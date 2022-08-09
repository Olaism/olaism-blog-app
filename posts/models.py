from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=255)
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