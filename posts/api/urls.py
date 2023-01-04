from django.urls import path

from . import views

urlpatterns = [
    path('posts', views.PostListAPIView.as_view()),
    path('posts/new/', views.PostCreateAPIView.as_view()),
    path('posts/<slug:slug>/', views.PostDetailAPIView.as_view())
]
