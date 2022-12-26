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
        return super(PublishedManager, self).get_queryset().filter(draft=False)


class Post(models.Model):

    title = models.CharField(max_length=100)
    highlight = models.CharField(max_length=255, default="", blank=True)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='posts'
    )
    image_url = models.URLField(null=True, blank=True)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    draft = models.BooleanField('Save as draft', default=True)
    featured = models.BooleanField(default=False)
    read_time = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    tags = TaggableManager()
    slug = models.SlugField(
        blank=True,
        null=True
    )
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ('-updated', '-publish')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

    def get_body_as_markdown(self):
        return mark_safe(markdown(self.body, safe_mode='escape'))


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = f"{slug}-{qs.first().id}"
        return create_slug(instance, new_slug=new_slug)
    return slug


@receiver(pre_save, sender=Post)
def pre_save_post_signal(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

    if instance.featured:
        qs = Post.objects.filter(featured=True)
        for post in qs:
            post.featured = False
            post.save()
