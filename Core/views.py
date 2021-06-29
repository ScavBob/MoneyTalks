from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView
from django_notification_system.models import NotificationTarget, TargetUserRecord
import plotly.graph_objs as go

from Core.forms import SignUpForm, SearchEventForm


class SignUpView(TemplateView):
    template_name = "Core/User/sign_up.html"

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            target = NotificationTarget.objects.get("Twilio")
            target_user_record = TargetUserRecord.objects.create(
                user_id=user,
                target_id=target,
                target_user_id=user.email,
                description=f"{user.first_name} {user.last_name}'s Notification",
                active=True
            )
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect('/profile/')
        else:
            context = {
                'form': form,
                'navbar': False,
            }
            return render(request, "Core/error.html", context)

    def get(self, request):
        form = SignUpForm()
        context = {
            'form': form,
            'navbar': False,
        }
        return render(request, self.template_name, context)


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = "Core/User/user.html"

    def get(self, request):
        profile = request.user.profile
        search = SearchEventForm()
        trace = go.Pie(labels=['Win', 'Lose', 'Tie'], values=profile.win_rate)
        data = [trace]
        fig = go.Figure(data=data)
        fig = fig.to_html()
        context = {
            'profile': profile,
            'navbar': True,
            'search': search,
            'fig': fig,
        }
        return render(request, self.template_name, context)
