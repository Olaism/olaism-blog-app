import os

from django import forms
from django.conf import settings
from django.core.mail import send_mail

class ContactForm(forms.Form):
    name = forms.CharField(max_length=120)
    your_email = forms.EmailField(required=True)
    inquiry = forms.CharField(max_length=70)
    message = forms.CharField(widget=forms.Textarea())

    def get_info(self):
        cl_data = super().clean()
        name = cl_data.get('name').strip()
        from_email = cl_data.get('your_email')
        subject = cl_data.get('inquiry')
        message = cl_data.get('message')

        msg = f"Hi, Olaism.\nMy name is {name} and my email is {from_email}."
        msg += f"\n\nSubject: {subject}\n\n"
        msg += f"\n{message}\n"
        msg += f"\nThanks."

        return subject, msg, from_email

    def send(self):
        subject, msg, from_email = self.get_info()
        send_mail(
            subject, 
            msg,
            os.environ.get('EMAIL_HOST_USER'),
            [os.environ.get('EMAIL_HOST_USER')])