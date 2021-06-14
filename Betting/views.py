from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.views.generic import TemplateView
from .models import Bet, Group, User, Event
from Core.forms import EventCreationForm, GroupCreationForm, BetCreationForm


# Create your views here.
class ActiveEventView(TemplateView):
    template_name = "Betting/Event/events.html"

    def get(self, request):
        event_list = reversed(Event.objects.all().order_by('-event_date', '-event_time'))
        group_list = Group.objects.filter()
        form = EventCreationForm()
        context = {
            'event_list': event_list,
            'group_list': group_list,
            'form': form,
            'var_active': True,
            'navbar': True,
        }
        return render(request, self.template_name, context)


class InactiveEventView(TemplateView):
    template_name = "Betting/Event/inactive_events.html"

    def get(self, request):
        event_list = Event.objects.all()
        group_list = Group.objects.all()
        form = EventCreationForm()
        context = {
            'event_list': event_list,
            'group_list': group_list,
            'form': form,
            'var_active': False,
            'navbar': True,
        }
        return render(request, self.template_name, context)


class CreateEvent(LoginRequiredMixin, TemplateView):

    def post(self, request):
        form = EventCreationForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            event.save()
            return HttpResponseRedirect('/event/' + str(event.id))
        else:
            return render(request, "Core/error.html", {'form': form})


class DeleteEvent(LoginRequiredMixin, TemplateView):

    def post(self, request, event_id):
        event = Event.objects.get(pk=event_id)
        if event.creator == request.user:
            event.delete()
            return HttpResponseRedirect('/')


class CreateGroup(LoginRequiredMixin, TemplateView):

    def post(self, request, event_id):
        form = GroupCreationForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.event_id = Event.objects.get(pk=event_id)
            group.save()
            group.refresh_from_db()
            group.member.add(request.user)
            group.save()
            return HttpResponseRedirect("/event/" + str(event_id))
        else:
            return render(request, "Core/error.html", {'form': form})


class EventDetailsView(TemplateView):
    template_name = "Betting/Event/details.html"

    def get(self, request, id):
        event = Event.objects.get(pk=id)
        group_list = Group.objects.filter(event_id=id)
        group_adding_form = GroupCreationForm()
        betting_on_group_form = BetCreationForm()
        bets = Bet.objects.filter(better=request.user)
        participated = False
        if request.user.id is None:
            participated = True

        for bet in bets:
            if bet.event == event:
                participated = True
                break

        if not participated:
            for group in group_list:
                if request.user in group.member.all():
                    participated = True
                    break

        context = {
            'event': event,
            'group_list': group_list,
            'group_adding_form': group_adding_form,
            'betting_on_group_form': betting_on_group_form,
            'participated': participated,
            'navbar': True,
        }
        return render(request, self.template_name, context)


class JoinGroup(TemplateView):

    def post(self, request, group_id):
        group = Group.objects.get(pk=group_id)
        group.member.add(request.user)
        return HttpResponseRedirect("/event/" + str(group.event_id.id))


class LeaveGroup(TemplateView):

    def post(self, request, group_id):
        group = Group.objects.get(pk=group_id)
        if group.member.count() == 1:
            group.delete()
        else:
            group.member.remove(request.user)
        return HttpResponseRedirect("/event/" + str(group.event_id.id))


class UserBetsView(TemplateView):
    template_name = "Betting/Event/events.html"

    def get(self, request, user_id):
        bets = Bet.objects.filter(better=user_id)
        events = []
        for bet in bets:
            events.append(bet.event)
        events.sort(reverse=True, key=eventSort)
        context = {
            'event_list': events,
            'group_list': Group.objects.all(),
            'navbar': True,
            'var_active': -1,
        }
        return render(request, self.template_name, context)


def eventSort(event):
    return datetime.combine(event.event_date, event.event_time)


class UserEventsView(LoginRequiredMixin, TemplateView):
    template_name = "Betting/Event/events.html"

    def get(self, request, user_id):
        groups = Group.objects.filter(member__in=[user_id])
        events = []
        for group in groups:
            events.append(group.event_id)
        events.sort(reverse=True, key=eventSort)
        context = {
            'event_list': events,
            'group_list': Group.objects.all(),
            'navbar': True,
            'var_active': -1,
        }
        return render(request, self.template_name, context)


class CreateBet(LoginRequiredMixin, TemplateView):

    def post(self, request, group_id):
        form = BetCreationForm(request.POST)
        if form.is_valid():
            group = Group.objects.get(pk=group_id)
            bet = form.save(commit=False)
            bet.event = group.event_id
            bet.betting_on = group
            bet.better = request.user
            bet.save()
            return HttpResponseRedirect('/event/' + str(group.event_id.id))