from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect

from BeanApp.errors import ErrMsg
from BeanApp.forms import SignUpForm, ContactForm, SignInForm, ChangeUserForm
from BeanApp.models import Comment


def signup(request):
    errList = []
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
        if User.objects.all().filter(username=usernameTemp).count() != 0:
            errList.append(ErrMsg.DUPLICATE_USER)
        if passwordTemp != password2Temp:
            errList.append(ErrMsg.PASSWORD_MISMATCH)
        if User.objects.all().filter(email=emailTemp).count() != 0:
            errList.append(ErrMsg.DUPLICATE_EMAIL)
        elif form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')

            password = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            email = form.cleaned_data.get("email")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            use = authenticate(request, username=username, password=password)
            login(request, user=use)
            return HttpResponseRedirect(redirect_to="/")

    return render(request, "signup.html", {
        "form": SignUpForm(),
        "errList": errList
    })


def login_(request):
    error = False
    if request.POST:
        username = request.POST.get("username")
        password = request.POST.get("password")
        print("login= user:", username)
        print("login= pass:", password)
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
        form = SignInForm(data=request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            if user:
                return HttpResponseRedirect(redirect_to="/")
        error = ErrMsg.WRONG_USERNAME_PASSWORD
    return render(request, "signup.html", {
        "form": SignInForm(data=request.POST or None),
        "error": error
    })


def contact_view(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            send_message = message + "email:" + from_email
            comment = Comment(subject=subject, email=from_email, message=message)
            comment.save()
            # try:
            #     send_mail(subject, send_message, from_email, ['‫‪ostaduj@fastmail.com‬‬'])
            # except Exception as exec:
            #     print("invalid email")
            error = ErrMsg.REQUEST_SENT
            return render(request, "ContactUs.html", {'form': form, "error": error})  # change text
    return render(request, "ContactUs.html", {'form': form})


def logout_(request):
    logout(request)
    return HttpResponseRedirect("/")


def edit_profile_form(request):
    if request.method == 'GET':
        form = ChangeUserForm()
    else:
        form = ChangeUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/userInfo')  # change text
    return render(request, "EditProfile.html", {'form': form})
    pass


def user_info(request):
    return render(request, "UserInfo.html", {"user": request.user})


def load_homepage(request):
    return render(request, "HomePage.html")
