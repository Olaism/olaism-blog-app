from django.urls import path

from .views import (
    PostListView, 
    PostDetailView,
    PostUpdateView,
    PostCreateView,
    PostDeleteView,
    PostSearchView,
    MyPostsView,
    status_change,
)

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('new/', PostCreateView.as_view(), name='post_create'),
    path('my-post/', MyPostsView.as_view(), name='my_posts'),
    path('search/', PostSearchView.as_view(), name='post_search'),
    path('<slug:slug>/status-change/', status_change, name='status_change'),
    path('<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('<slug:slug>/edit/', PostUpdateView.as_view(), name="post_update"),
    path('<slug:slug>/delete/', PostDeleteView.as_view(), name="post_delete"),
    path('<tag_slug>/', PostListView.as_view(), name="post_list_by_tag"),
]