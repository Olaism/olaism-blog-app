import markdown
from datetime import (
    date,
    timedelta
)

from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe

from ..models import Post

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag('includes/latest_posts.html')
def show_trending_posts(count=5):
    end_date = date.today()
    start_date = end_date - timedelta(days=7)
    trending_posts = Post.published.filter(
        publish__range=[start_date, end_date]).order_by('-views')[:count]
    return {'trending_posts': trending_posts}

# @register.assignment_tag
# def get_most_commented_posts(count=5):
#     return Post.published.annotate(
#         total_comments=Count('comments')
#     ).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
