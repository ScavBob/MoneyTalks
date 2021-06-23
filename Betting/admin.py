from django.contrib import admin
from .models import Event, Profile, Bet, Group, EventType
# Register your models here.
admin.site.register(Event)
admin.site.register(Bet)
admin.site.register(Profile)
admin.site.register(Group)
admin.site.register(EventType)