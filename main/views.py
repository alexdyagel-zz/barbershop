from django.shortcuts import render, redirect
from django.urls import reverse

from main.forms import RegistrationForm


def index(request):
    return render(request, 'main/home.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('main:home'))
    else:
        form = RegistrationForm()

        args = {'form': form}
        return render(request, 'main/reg_form.html', args)
