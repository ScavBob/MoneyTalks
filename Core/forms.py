from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from Betting.models import Event, Group, Bet, EventType


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


class UserProfileUpdate(forms.ModelForm):
    picture = forms.ImageField(required=False)
    winner_speech = forms.CharField(required=False)
    username = forms.CharField(required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.CharField(required=False)
    password = forms.PasswordInput()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')


class EventTypeCreationForm(forms.ModelForm):

    class Meta:
        model = EventType
        fields = ('type', 'image')