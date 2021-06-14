from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView

from Core.forms import SignUpForm


class SignUpView(TemplateView):
    template_name = "Core/User/sign_up.html"

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.name = form.cleaned_data.get("name")
            user.profile.surname = form.cleaned_data.get("surname")
            user.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect('/profile/')
        else:
            context = {
                'form': form,
                'navbar' : False,
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
        context = {
            'profile': profile,
            'navbar': True,
        }
        return render(request, self.template_name, context)