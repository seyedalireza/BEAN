from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect

from BeanApp.forms import SignUpForm, ContactForm, SignInForm


def signup(request):
    users = User.objects.all()
    if request.method == 'GET':
        return render(request, "signup.html", {
            "form": SignUpForm(),
        })
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        usernameTemp = form.data.get('username')
        passwordTemp = form.data.get('password1')
        password2Temp = form.data.get('password2')
        emailTemp = form.data.get("email")
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            email = form.cleaned_data.get("email")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            form.save()
            new_user = User(password=password, username=username, last_name=last_name, email=email,
                            first_name=first_name)
            new_user.save()
            authenticate(request, username=username, password=password)
            return HttpResponseRedirect(redirect_to="/")
    error = ""
    try:
        if users.get(username=username):
            error += "کاربری با نام کاربری وارد شده وجود دارد"
    except Exception as s:
        print(s)
    if passwordTemp != password2Temp:
        error += "گذرواژه و تکرار آن یکسان نیستند"
    if users.get(email=emailTemp):
        error += "کاربری با ایمیل داده شده وجود دارد"
    return render(request, "signup.html", {
        "form": SignUpForm(),
        "error": error
    })


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
    return render(request, "LoginPage.html", {
        "error": error
    })


def loginWithForm(request):
    error = "nothing"
    users = User.objects.all()
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            form.save()  # todo change id
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            return HttpResponseRedirect(redirect_to="/")
    return render(request, "signup.html", {
    "form": SignInForm(),
    "error": error
})


def contact_view(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            send_message = message + "email:" + from_email
            try:
                send_mail(subject, send_message, from_email, ['‫‪ostaduj@fastmail.com‬‬'])
            except Exception as exec:
                print("invalid email")
            return redirect('success')  # change text
    return render(request, "email.html", {'form': form})


def logout_(request):
    logout(request)
    return HttpResponseRedirect("/")


def loadHomepage(request):
    return render(request, "HomePage.html")


def loadSignup(request):
    return None
