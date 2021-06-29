from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from Betting.models import Event, Group, Bet
from django import forms
from django.forms import ModelForm, DateTimeField, DateTimeInput


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


class EventCreationForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('description', 'event_date', 'event_time', 'event_type')
        widgets = {'event_date': DateInput(),
                   'event_time': TimeInput()}


class GroupCreationForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('group_name', 'group_bet_amount', 'group_bet')


class BetCreationForm(forms.ModelForm):
    class Meta:
        model = Bet
        fields = ('amount', 'item')


class SearchEventForm(forms.ModelForm):
    description = forms.CharField(label='')

    class Meta:
        model = Event
        fields = ('description',)
