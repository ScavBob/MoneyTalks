from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Bet, Group, User, Event
from Core.forms import EventCreationForm, GroupCreationForm, BetCreationForm, SearchEventForm


# Create your views here.
def eventSort(event):
    return datetime.combine(event.event_date, event.event_time)


class ExtendedTemplateView(TemplateView):
    search = SearchEventForm()
    navbar = True


class ActiveEventView(ExtendedTemplateView):
    template_name = "Betting/Event/active_events.html"

    def get(self, request):
        event_list = reversed(Event.objects.all().order_by('-event_date', '-event_time'))
        group_list = Group.objects.filter()
        event_bets = Bet.objects.all()
        form = EventCreationForm()

        context = {
            'event_list': event_list,
            'group_list': group_list,
            'bet_list': event_bets,
            'form': form,
            'var_active': True,
            'navbar': self.navbar,
            'search': self.search,
        }
        return render(request, self.template_name, context)


class InactiveEventView(ExtendedTemplateView):
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
            'navbar': self.navbar,
            'search': self.search,
        }
        return render(request, self.template_name, context)


class CreateEvent(LoginRequiredMixin, ExtendedTemplateView):

    def post(self, request):
        form = EventCreationForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            event.save()
            return HttpResponseRedirect('/event/' + str(event.id))
        else:
            return render(request, "Core/error.html", {'form': form})


class DeleteEvent(LoginRequiredMixin, ExtendedTemplateView):

    def post(self, request, event_id):
        event = Event.objects.get(pk=event_id)
        if event.creator == request.user:
            event.delete()
            return HttpResponseRedirect('/')


class CreateGroup(LoginRequiredMixin, ExtendedTemplateView):

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


class SearchEventView(ExtendedTemplateView):
    template_name = "Betting/Event/active_events.html"

    def get(self, request):
        return HttpResponseRedirect("/")

    def post(self, request):
        event_search = SearchEventForm(request.POST)
        if event_search.is_valid():
            search_string = event_search.cleaned_data['description']
            people = User.objects.filter(username__contains=search_string)
            people_groups = Group.objects.filter(member__in=people)
            desc_filter = Event.objects.filter(description__contains=search_string)
            type_filter = Event.objects.filter(event_type__contains=search_string)
            group_list = Group.objects.filter()
            event_bets = Bet.objects.all()
            all_events = []

            for event in desc_filter:
                all_events.append(event)

            for event in type_filter:
                if event not in all_events:
                    all_events.append(event)

            for group in group_list:
                if search_string in group.group_name or search_string in group.group_bet:
                    if group.event_id not in all_events:
                        all_events.append(group.event_id)

            for bet in event_bets:
                if search_string in bet.item:
                    if bet.event not in all_events:
                        all_events.append(bet.event)

            for group in people_groups:
                if group.event_id not in all_events:
                    all_events.append(group.event_id)
            all_events.sort(reverse=True, key=eventSort)
            context = {
                'event_list': all_events,
                'group_list': group_list,
                'bet_list': event_bets,
                'var_active': -1,
                'navbar': self.navbar,
                'search': self.search,
            }
            return render(request, self.template_name, context)


class EventDetailsView(ExtendedTemplateView):
    template_name = "Betting/Event/details.html"

    def get(self, request, id):
        event = Event.objects.get(pk=id)
        group_list = Group.objects.filter(event_id=id)
        group_adding_form = GroupCreationForm()
        betting_on_group_form = BetCreationForm()
        bets = Bet.objects.filter(better=request.user)
        event_bets = Bet.objects.filter(event=id)
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
            'bet_list': event_bets,
            'group_adding_form': group_adding_form,
            'betting_on_group_form': betting_on_group_form,
            'participated': participated,
            'navbar': self.navbar,
            'search': self.search,
        }
        return render(request, self.template_name, context)


class JoinGroup(ExtendedTemplateView):

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


class UserBetsView(ExtendedTemplateView):
    template_name = "Betting/Event/active_events.html"

    def get(self, request):
        bets = Bet.objects.filter(better=request.user.id)
        events = []
        for bet in bets:
            events.append(bet.event)
        events.sort(reverse=True, key=eventSort)
        context = {
            'event_list': events,
            'group_list': Group.objects.all(),
            'var_active': -1,
            'navbar': self.navbar,
            'search': self.search,
        }
        return render(request, self.template_name, context)


class UserEventsView(LoginRequiredMixin, ExtendedTemplateView):
    template_name = "Betting/Event/active_events.html"

    def get(self, request):
        groups = Group.objects.filter(member__in=[request.user])
        events = []
        for group in groups:
            events.append(group.event_id)
        events.sort(reverse=True, key=eventSort)
        context = {
            'event_list': events,
            'group_list': Group.objects.all(),
            'var_active': -1,
            'navbar': self.navbar,
            'search': self.search,
        }
        return render(request, self.template_name, context)


class CreateBet(LoginRequiredMixin, ExtendedTemplateView):

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


class RemoveBet(LoginRequiredMixin, ExtendedTemplateView):

    def post(self, request, bet_id):
        bet = Bet.objects.get(pk=bet_id)
        event_id = bet.event_id
        bet.delete()
        return HttpResponseRedirect('/event/' + str(event_id))
