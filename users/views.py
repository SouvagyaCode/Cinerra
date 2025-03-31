from django.shortcuts import render
from .forms import signupform
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login ,logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def home(request):
    return render(request, 'base.html')


def signup(request):
    if request.method == 'POST':
        form = signupform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signin')
    else:
        form = signupform()
    return render(request, 'signup.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user :
            login(request, user)
            # print('login success')
            return redirect('home')
        else:
            return redirect('signin')
        
    return render(request, 'signin.html')

def user_logout(request):
    logout(request)
    return redirect('signin')