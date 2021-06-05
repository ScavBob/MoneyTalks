from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views.generic import TemplateView
from .models import Bet, Group, User, Event


# Create your views here.
def index(request):
    event_list = Event.objects.all()
    group_list = Group.objects.all()
    template = loader.get_template('Betting/main_menu.html')
    context = {
        'event_list'    : event_list,
        'group_list'    : group_list,
    }
    return HttpResponse(template.render(context, request))
