from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    slug = models.SlugField(
        max_length=30,
        unique=True,
        null=True,
        blank=True,
    )
    
    def get_absolute_url(self):
        return reverse('user_detail', kwargs={'slug': self.slug})

@receiver(pre_save, sender=CustomUser)
def add_slug_to_customuser(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.username)