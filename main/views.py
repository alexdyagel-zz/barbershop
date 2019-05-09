from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from main.forms import RegistrationForm


def index(request):
    if request.user.is_authenticated:
        return render(request, 'main/barbershop.html')
    else:
        return redirect(reverse('main:login'))


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('main:home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/registration.html', {'form': form})
