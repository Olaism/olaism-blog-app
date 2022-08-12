from django.urls import path

from .views import (
    SignupView,
    Profile,
    UserDetailView
)

urlpatterns = [
    path('<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('profile/', Profile.as_view(), name='my_profile'),
]