from today.views import bookmark
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserForm, LoginForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from today.models import *

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:            
            return redirect('signup')
    else:
        form = UserForm()
        return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse('로그인 실패. 다시 시도 해보세요.')
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def mypage(request):
    logged_in_user = request.user
    logged_in_user_posts = Post.objects.filter(author=request.user)
    logged_in_user_bookmarks=Post.objects.filter(bookmark=request.user)
    return render(request, 'mypage.html', {'posts': logged_in_user_posts, 'bookmarks':logged_in_user_bookmarks})

