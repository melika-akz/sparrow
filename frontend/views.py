from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def index(request):
    return render(request, 'frontend/index.html')

def login(request):
    if request.user.is_authenticated:
        return redirect('/home/')
    context = {
        'google_client_id': settings.GOOGLE_CLIENT_ID
    }
    return render(request, 'frontend/login.html', context)

def signup(request):
    if request.user.is_authenticated:
        return redirect('/home/')
    return render(request, 'frontend/signup.html')

