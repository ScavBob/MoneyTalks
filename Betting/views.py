from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.views.generic import TemplateView
from .models import Bet, Group, User, Event
from Core.forms import EventCreationForm, GroupCreationForm


# Create your views here.
class ActiveEventView(TemplateView):
    template_name = "Betting/Event/events.html"

    def get(self, request):
        event_list = Event.objects.all()
        group_list = Group.objects.filter()
        form = EventCreationForm()
        context = {
            'event_list': event_list,
            'group_list': group_list,
            'form': form,
            'var_active': True,
        }
        return render(request, self.template_name, context)


class InactiveEventView(TemplateView):
    template_name = "Betting/inactive_events.html"

    def get(self, request):
        event_list = Event.objects.all()
        group_list = Group.objects.filter()
        form = EventCreationForm()
        context = {
            'event_list': event_list,
            'group_list': group_list,
            'form': form,
            'var_active' : False,
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
        form = GroupCreationForm()
        already_in_group = False
        if request.user.id is None:
            already_in_group = True

        for group in group_list:
            if request.user in group.member.all():
                already_in_group = True
                break

        context = {
            'event': event,
            'group_list': group_list,
            'form': form,
            'already_in_group': already_in_group,
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


class BetView(TemplateView):
    template_name = "Betting/bet.html"

    def get(self, request, bet_id):
        bet = Bet.objects.get(pk = bet_id)
        context={
            "bet":bet,
        }
        return render(request, self.template_name, context)