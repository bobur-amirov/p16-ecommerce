from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from .forms import RegisterForm

User = get_user_model()


def register(request):
    if request.method == 'POST':
        user = RegisterForm(request.POST)
        print('registerga utvotti')
        if user.is_valid():
            user.save()
            username = user.cleaned_data['username']
            password = user.cleaned_data['username']
            user_login = authenticate(request,username=username, password=password)
            login(request, user_login)
            messages.success(request, 'You are successfully registered!')
            return redirect('product:home')
    else:
        user = RegisterForm()
    return render(request, 'account/register.html', {'form': user})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You are successfully logined!')
            return redirect('product:home')
        else:
            messages.warning(request, 'Not logined! There was an error!')
            return redirect('login_user')

    return render(request, 'account/login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, 'You are successfully logged out!')
    return redirect('product:home')
