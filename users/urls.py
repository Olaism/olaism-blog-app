from django.urls import path

from .views import (
    SignupView,
    Profile,
)

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('profile/', Profile.as_view(), name='my_profile'),
]