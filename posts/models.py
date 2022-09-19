from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils.html import mark_safe
from django.db.models.signals import pre_save
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

    title = models.CharField(max_length=30, unique=True)
    highlight = models.CharField(max_length=255, default="", blank=True)
    author = models.ForeignKey(
        get_user_model(), 
        on_delete = models.CASCADE,
        related_name = 'posts'
    )
    image_url = models.URLField(null=True, blank=True)
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
        unique=True,
        max_length=30, 
        blank=True, 
        null= True
    )
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})
        
    def get_body_as_markdown(self):
        return mark_safe(markdown(self.body, safe_mode='escape'))

@receiver(pre_save, sender=Post)
def add_slug_to_model(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)