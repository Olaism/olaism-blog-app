from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from .forms import ContactForm

class HomePageView(TemplateView):
    template_name = 'pages/home.html'

class ContactPageView(FormView):
    template_name = 'pages/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact_success')

    def form_valid(self, form):
        form.send()
        return super().form_valid(form)

class ContactSuccessView(TemplateView):
    template_name = 'pages/contact_success.html'