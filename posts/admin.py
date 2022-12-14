from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publish', 'draft', 'slug',)
    list_filter = ('created', 'publish', 'author')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ['publish']

admin.site.register(Post, PostAdmin)