from django import forms
from django.conf.locale import id
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField( max_length=30, required=False, help_text='Optional' ,widget=forms.TextInput(attrs = {
        "" : "id_first_name" , "name" : "نام"}))
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.',widget=forms.TextInput(attrs = {
        "id" : "id_first_name" , "name" : "نام"}))
    email = forms.EmailField(max_length=254 ,  id = "id_email", help_text='Required. Inform a valid email address.' , widget=forms.TextInput(attrs = {
        "id" : "id_first_name" , "name" : "نام"}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class ContactForm(forms.Form):
    from_email = forms.EmailField(required=False, max_length=250 , min_length=10)
    subject = forms.CharField(required=True, max_length=250 , min_length=10)
    message = forms.CharField(widget=forms.Textarea, required=True, max_length=250 , min_length=10)