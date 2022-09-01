from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from taggit.models import Tag
from posts.models import Post
from .forms import ContactForm

class HomePageView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['posts'] = Post.objects.filter(status='published')
        context['tags'] = Tag.objects.all()
        context['featured'] = Post.objects.filter(featured=True).first()
        return context

class ContactPageView(FormView):
    template_name = 'pages/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact_success')

    def form_valid(self, form):
        form.send()
        return super().form_valid(form)

class ContactSuccessView(TemplateView):
    template_name = 'pages/contact_success.html'