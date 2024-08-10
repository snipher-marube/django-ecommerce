from django.shortcuts import render

def user_register(request):
    return render(request, 'accounts/register.html')

def user_login(request):
    return render(request, 'accounts/login.html')
