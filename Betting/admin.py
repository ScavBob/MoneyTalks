from django.contrib import admin
from .models import Event, User, Bet, PlacedBet, BetForEvent, Participates
# Register your models here.
admin.site.register(Event)
admin.site.register(Bet)
admin.site.register(User)