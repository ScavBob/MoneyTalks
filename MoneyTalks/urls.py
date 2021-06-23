"""MoneyTalks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

import Betting.views
import Core.views
from MoneyTalks import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Betting.views.ActiveEventView.as_view(), name="events"),
    path('search/', Betting.views.SearchEventView.as_view(), name="events"),
    path('previousEvents/', Betting.views.InactiveEventView.as_view(), name="previous_events"),
    path('signup/', Core.views.SignUpView.as_view(), name="signup"),
    path('profile/', Core.views.UserProfileView.as_view(), name="profile"),
    path('login/', LoginView.as_view(template_name="Core/User/login.html"), name='login'),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('addEvent/', Betting.views.CreateEvent.as_view(), name="create_event"),
    path('removeEvent/<int:event_id>', Betting.views.DeleteEvent.as_view(), name="delete_event"),
    path('active_event/<int:id>/', Betting.views.ActiveEventDetailsView.as_view(), name="active_event_details"),
    path('inactive_event/<int:id>/', Betting.views.InactiveEventDetailsView.as_view(), name="inactive_event_details"),
    path('addGroup/<int:event_id>', Betting.views.CreateGroup.as_view(), name="create_group"),
    path('event/join/<int:group_id>', Betting.views.JoinGroup.as_view(), name='join_group'),
    path('event/leave/<int:group_id>', Betting.views.LeaveGroup.as_view(), name='join_group'),
    path('bets/', Betting.views.UserBetsView.as_view(), name="user_bets"),
    path('events/', Betting.views.UserEventsView.as_view(), name="user_events"),
    path('addBet/<int:group_id>', Betting.views.CreateBet.as_view(), name="create_bet"),
    path('removeBet/<int:bet_id>', Betting.views.RemoveBet.as_view(), name="remove_bet"),

]
