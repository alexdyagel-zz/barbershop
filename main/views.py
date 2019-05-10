from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.core import serializers
from django.shortcuts import render, redirect
from django.urls import reverse
from formtools.wizard.views import SessionWizardView

from main.forms import FirstStepOrder, SecondStepOrder, ThirdStepOrder
from main.models import Seance, Order


def index(request):
    if request.user.is_authenticated:
        return render(request, 'main/barbershop.html')
    else:
        return redirect(reverse('main:login'))


def order(request):
    return render(request, 'main/order.html')


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


def step1(request):
    if request.method == 'POST':
        form = FirstStepOrder(request.POST)
        if form.is_valid():
            service = form.cleaned_data['service']
            specialist = form.cleaned_data['specialist']
            seances = Seance.objects.filter(specialist=specialist).order_by('date')
            print(type(seances))
            request.session['service'] = serializers.serialize('json', [service])
            request.session['seances'] = serializers.serialize('json', seances)
            print(request.session['seances'])
            print(request.session['service'])
            return redirect('main:order2')
    else:
        form = FirstStepOrder()
    return render(request, 'main/order.html', {'form': form})


def step2(request):
    des_seances = serializers.deserialize("json", request.session['seances'])
    seances = [seance.object for seance in des_seances]
    if request.method == 'POST':
        form = SecondStepOrder(request.POST, seances=seances)
        if form.is_valid():
            date = form.cleaned_data['date']
            seances_ids = [seance.id for seance in seances]
            seances = Seance.objects.filter(date=date, id__in=seances_ids).order_by('time')
            request.session['seances'] = serializers.serialize('json', seances)
            return redirect('main:order3')
    else:
        form = SecondStepOrder(seances=seances)
    return render(request, 'main/order2.html', {'form': form})


def step3(request):
    des_seances = serializers.deserialize("json", request.session['seances'])
    seances = [seance.object for seance in des_seances]
    print(seances)
    if request.method == 'POST':
        form = ThirdStepOrder(request.POST, seances=seances)
        if form.is_valid():
            time = form.cleaned_data['time']
            print(time)
            seances_ids = [seance.id for seance in seances]
            print(seances_ids)
            seance = Seance.objects.get(time=time, id__in=seances_ids)
            print(seance)
            service = list(serializers.deserialize("json", request.session['service']))[0].object
            print(service)
            order = Order(seance=seance, service=service, user=request.user)
            order.save()
            return redirect('main:home')
    else:
        print(seances)
        form = ThirdStepOrder(seances=seances)
    return render(request, 'main/order3.html', {'form': form})


class FormWizardView(SessionWizardView):
    template_name = "main/order.html"
    form_list = [FirstStepOrder, SecondStepOrder, ThirdStepOrder]

    def done(self, form_list, **kwargs):
        return render(self.request, 'main/barbershop.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })
