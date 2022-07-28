from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.views.generic import TemplateView

# import random

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            auth_login(request, user)
            # celery.delay(user = user)
            return redirect('dashboard:home')
    else:
        form = SignUpForm()
    return render(request, 'backend/accounts/register.html', {'form': form})






