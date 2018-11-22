from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from BeanApp.forms import SignUpForm


def signup(request):
    error = False
    users = User.objects.all()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()#todo change id
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            password2 = form.cleaned_data.get('password2')
            email = form.cleaned_data.get("email")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            if users.get(username=username):
                error = True
            if password != password2:
                error = True
            if username != email:
                error = True
            #todo retuen render for signUppage if error is true for each if
            if not error:
                new_user = User(password=password, username=username, last_name=last_name, email=email,
                            first_name=first_name)
                new_user.save()
        return HttpResponseRedirect(redirect_to="/")


def login(request):
    error = False
    if request.POST:
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect("/")
            else:
                error = True
        error = True
    return render(request, "login_form.html", {
        "error": error
    })
