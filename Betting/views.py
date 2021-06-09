from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views.generic import TemplateView
from .models import Bet, Group, User, Event


# Create your views here.
class EventView(TemplateView):
    template_name = "Betting/main_menu.html"

    def get(self, request):
        event_list = Event.objects.all()
        group_list = Group.objects.all()
        context = {
            'event_list'    : event_list,
            'group_list'    : group_list,
        }
        return render(request, self.template_name, context)
