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
        from_email = cl_data.get('email')
        subject = cl_data.get('inquiry')

        msg = f"Hi, Olaism.\nMy name is {name} and my email is {from_email}."
        msg += f"\n{subject}\n\n"
        msg += f"\n{cl_data.get('message')}"
        msg += f"\nThanks."

        return subject, msg, from_email

    def send(self):

        send_mail(
            subject, 
            msg,
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER])