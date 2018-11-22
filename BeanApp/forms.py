from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    GROUP_CHOICES = [
        ('id_type_0', 'Teacher'),
        ('id_type_1', 'Student'),
    ]
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    type = forms.ChoiceField(choices=GROUP_CHOICES, widget=forms.RadioSelect())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


class SignInForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class ContactForm(forms.Form):
    email = forms.EmailField()
    subject = forms.CharField(required=True, max_length=250, min_length=10,
                              widget=forms.TextInput(attrs={"id": "id_title"}))
    message = forms.CharField(required=True, max_length=250, min_length=10,
                              widget=forms.Textarea(attrs={"id": "id_text"}))

class ChangeUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("first_name", 'last_name',)
