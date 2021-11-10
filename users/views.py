from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from . import models
from .forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("/")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = UserCreationForm()
        return render(
            request=request,
            template_name="users/signup.html",
            context={"register_form": form},
        )


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {user.name}.")
                if request.GET.get("next") is not None:
                    return redirect(request.GET.get("next"))
                else:
                    return redirect("/")
            else:
                messages.error(request, "Invalid username or password.")
                return redirect("/accounts/login")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("/accounts/login")
    else:
        form = AuthenticationForm()
        return render(
            request=request,
            template_name="users/login.html",
            context={"login_form": form},
        )


def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/")


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data["email"]
            associated_users = models.User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "users/password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        "domain": "pmi-seg2501.herokuapp.com",
                        "site_name": "Website",
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        "token": default_token_generator.make_token(user),
                        "protocol": "http",
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(
                            subject,
                            email,
                            "afeti047@uottawa.ca",
                            [user.email],
                            fail_silently=False,
                        )
                    except BadHeaderError:
                        return HttpResponse("Invalid header found.")
                    return redirect("/accounts/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(
        request=request,
        template_name="users/password/password_reset.html",
        context={"password_reset_form": password_reset_form},
    )
