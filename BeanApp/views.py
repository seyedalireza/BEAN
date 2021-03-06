from sqlite3.dbapi2 import Time

from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User, Group
from django.core.handlers import exception
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.safestring import mark_safe
from markdown import markdown

# Create your views here.
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect

from BeanApp import errors
from BeanApp.errors import ErrMsg
from BeanApp.forms import SignUpForm, ContactForm, SignInForm, ChangeUserForm, FreeTimeSaveForm
from BeanApp.models import Comment, Person, TeacherFreeTime


def signup(request):
    errList = []
    if request.method == 'GET':
        return render(request, "signup.html", {
            "form": SignUpForm(),
        })
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        username_temp = form.data.get('username')
        password_temp = form.data.get('password1')
        password2_temp = form.data.get('password2')
        email_temp = form.data.get("email")
        print(username_temp)
        print(password_temp)
        print(password2_temp)
        print(email_temp)
        if User.objects.all().filter(username=username_temp).count() != 0:
            errList.append(ErrMsg.DUPLICATE_USER)
        if password_temp != password2_temp:
            errList.append(ErrMsg.PASSWORD_MISMATCH)
        if User.objects.all().filter(email=email_temp).count() != 0:
            errList.append(ErrMsg.DUPLICATE_EMAIL)
        print(form.is_valid())
        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            print(username)
            print(password)
            print(email)
            user = authenticate(request, username=username, password=password)
            print("khar1")
            login(request, user=user)
            item = form.cleaned_data.get("type").replace("id_type_", "")
            my_group = Group.objects.get(name=form.GROUP_CHOICES[int(item)][1])
            my_group.user_set.add(user)
            user = User.objects.get(username=username)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            person = Person(user=request.user)
            person.save()
            return HttpResponseRedirect(redirect_to="/")

    return render(request, "signup.html", {
        "form": SignUpForm(),
        "errList": errList
    })


def login_with_form(request):
    error = "nothing"
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
    return render(request, "login.html", {
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
            try:
                send_mail(subject="sdafdsafasdf",message= "adsfghfsaf" ,from_email = "svafaiet@gmail.com",recipient_list = ['‫‪ostadju@fastmail.com‬‬','seidalirezahosseini@gmail.com' ])
            except Exception as exec:
                print("invalid email")
            error = ErrMsg.REQUEST_SENT
            return render(request, "ContactUs.html", {'form': form, "error": error})  # change text
    return render(request, "ContactUs.html", {'form': form})


def logout_(request):
    logout(request)
    return HttpResponseRedirect("/")


def edit_profile(request):
    person = get_Person_from_user(request)
    if request.method == 'GET':
        form = ChangeUserForm()
    else:
        form = ChangeUserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            bio = form.cleaned_data.get('bio')
            gender = form.cleaned_data.get('gender')
            # person.picture = request.FILES['picture']
        
            bio = markdown(bio)
            person.bio = bio
            person.gender = gender
            if request.user:
                user = Person.objects.get(user=request.user)
                user.bio = bio
                user.gender = gender
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                person.user.first_name = first_name
                person.user.last_name = last_name
                person.user.save()
                user.save()
            person.save()
            return HttpResponseRedirect('/userInfo', {"person": person, "user": request.user})  # change text
    return render(request, "EditProfile.html", {'form': form})


def user_info(request):
    person = get_Person_from_user(request)
    return render(request, "UserInfo.html", {"person": person, "user": request.user})


def get_Person_from_user(request):
    if request.user.is_authenticated:
        try:
            person = request.user.person
        except:
            person = Person(user=request.user)
            person.bio = " "
            person.save()
    else:
        person = ""
    return person


def load_homepage(request):
    return render(request, "HomePage.html")


def remove_user(request):
    User.objects.filter(pk=request.user.pk).update(is_active=False)
    User.objects.filter(pk=request.user.pk).delete()
    return HttpResponseRedirect('/')


def send_free_time(request):
    person = get_Person_from_user(request)
    if request.method == 'GET':
        form = FreeTimeSaveForm()
    else:
        form = FreeTimeSaveForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            try:
                if Time(form.data.get("start")) > Time(form.data.get("end")):
                    form.errors["start"][0] = errors.ErrMsg.INVALID_TIME_ORDER
                    return render(request, "signup.html", {'form': form})
            except Exception as e3:
                print(e3.__str__())
            return HttpResponseRedirect('/')  # change text
        else:
            try:
                if form.errors["start"][0] is not None:
                    form.errors["start"][0] = errors.ErrMsg.WRONG_TIME_START
            except Exception as e1:
                print(e1.__str__())
            try:
                if form.errors["end"] is not None:
                    form.errors["end"][0] = errors.ErrMsg.WRONG_TIME_END
            except Exception as e2:
                print(e2.__str__())
            try:
                if form.errors["date"][0] is not None:
                    form.errors["date"] = errors.ErrMsg.WRONG_DATE
            except Exception as e4:
                print(e4.__str__())
        # TeacherFreeTime.objects.filter(person=request.user.person, date=form.data.get("date"))
    return render(request, "signup.html", {'form': form})
