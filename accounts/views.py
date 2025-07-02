from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from accounts.forms import LoginForm


# Create your views here.
def login_view(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            remember_me = form.cleaned_data.get("remember_me")
            user = authenticate(request, username=username, password=password)

            if user:
                if remember_me:
                    request.session.set_expiry(7 * 24 * 60 * 60)
                else:
                    request.session.set_expiry(0)
                login(request, user)
                return redirect("main:home")

    return render(request, 'accounts/login_page.html', {"form": form})


def register_view(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("main:home")
    return render(request, "accounts/register_page.html", {"form": form})
