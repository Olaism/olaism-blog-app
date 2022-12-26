from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.views.generic import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView
)

from .forms import CustomUserCreationForm

class SignupView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

class UserDetailView(DetailView):
    model = get_user_model()
    template_name = 'user_detail.html'
    context_object_name = 'user'
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['published_posts'] = self.object.posts.filter(draft=False)
        return context

class Profile(UpdateView):
    model = get_user_model()
    fields = ("first_name", 'last_name', 'email',)
    template_name = 'profile.html'
    success_url = reverse_lazy('my_profile')

    def get_object(self):
        return self.request.user