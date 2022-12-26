from django.urls import path

from .views import (
    HomePageView,
    ContactPageView,
    ContactSuccessView,
    PostListView,
)

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
    path('contact/', ContactPageView.as_view(), name="contact"),
    path('contact/success/', ContactSuccessView.as_view(), name="contact_success"),
    path('', PostListView.as_view(), name='post_list'),
    path('tag/<slug:tag_slug>/', PostListView.as_view(), name='post_tag_list'),
    path('search/<str:search_term>/',
         PostListView.as_view(), name='post_search_list'),
]
