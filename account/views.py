from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


def register(request):
    if request.method == 'POST':
        user = UserCreationForm(request.POST)
        if user.is_valid():
            user.save()
            username = user.cleaned_data['username']
            password = user.cleaned_data['username']
            user_login = authenticate(username=username, password=password)
            login(request, user_login)
            messages.success(request, 'You are successfully registered!')
            return redirect('product:home')

    return render(request, 'account/register.html', {})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('product:home')
        else:
            messages.error(request, 'Not logined! There was an error!')
            return redirect('login_user')

    return render(request, 'account/login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, 'You are successfully logged out!')
    return redirect('product:home')
