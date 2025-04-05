from django.shortcuts import render

def index(request):
    return render(request, 'frontend/index.html')

def login(request):
    return render(request, 'frontend/login.html')

def signup(request):
    return render(request, 'frontend/signup.html')

