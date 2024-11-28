from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from account.forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib import messages


def index(request):
    return render(request, "index.html")


def user_login(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("index")
        else:
            return render(
                request,
                "account/login.html",
                {"form": form, "error": "Invalid credentials"},
            )
    else:
        form = CustomAuthenticationForm()
    return render(request, "account/login.html", {"form": form})


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(
                request, f"Account created for {username}! You can now log in."
            )
            return redirect("account:login")
    else:
        form = CustomUserCreationForm()
    return render(request, "account/register.html", {"form": form})


@login_required
def user_logout(request):
    logout(request)
    return redirect("account:login")
