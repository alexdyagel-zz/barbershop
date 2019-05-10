from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from main.models import Specialist, Service


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class FirstStepOrder(forms.Form):
    specialist = forms.ModelChoiceField(queryset=Specialist.objects.all())
    service = forms.ModelChoiceField(queryset=Service.objects.all())


class SecondStepOrder(forms.Form):
    def __init__(self, *args, **kwargs):
        self.seances = None
        if kwargs:
            self.seances = kwargs.pop('seances')
        super().__init__(*args, **kwargs)
        if self.seances:
            list_of_dates = sorted(list({seance.date for seance in self.seances}))
            self.fields['date'].choices = [(date, date) for date in list_of_dates]

    date = forms.ChoiceField(widget=forms.Select())


class ThirdStepOrder(forms.Form):
    def __init__(self, *args, **kwargs):
        self.seances = None
        if kwargs:
            self.seances = kwargs.pop('seances')
        super().__init__(*args, **kwargs)
        if self.seances:
            list_of_times = sorted(list({seance.time for seance in self.seances}))
            self.fields['time'].choices = [(time, time) for time in list_of_times]

    time = forms.ChoiceField(widget=forms.Select())
