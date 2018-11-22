from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('id_username', 'id_first_name', 'id_last_name', 'id_email', 'id_password_1', 'id_password_2',)


class ContactForm(forms.Form):
    from_email = forms.EmailField(required=False, max_length=250, min_length=10)
    subject = forms.CharField(required=True, max_length=250, min_length=10)
    message = forms.CharField(widget=forms.Textarea, required=True, max_length=250, min_length=10)
