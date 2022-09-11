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
    path('<int:pk>/status-change/', status_change, name='status_change'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name="post_update"),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name="post_delete"),
    path('<tag_slug>/', PostListView.as_view(), name="post_list_by_tag"),
]