from django.db import models
from django.http import HttpResponse
from django.db.models.functions import Now


# Create your models here.
class Bet(models.Model):
    id = models.AutoField()
    id.primary_key = True
    amount = models.IntegerField(null=False)
    item = models.IntegerField(null=False)
    event = models.ForeignKey("Event", on_delete=models.CASCADE)
    bet_item = models.ForeignKey("ItemType", on_delete=models.CASCADE)
    creation_time = models.DateTimeField(Now())
    change_time = models.DateTimeField(creation_time.minute + 5)


class Group(models.Model):
    id = models.AutoField()
    id.primary_key = True
    groupies = models.ManyToManyField("User", related_name="Group_Members", )


class User(models.Model):
    id = models.AutoField()
    id.primary_key = True
    #picture
    #winrate
    #old bets
    #current bets
    #password
    name = models.CharField(max_length=100)
    bets = models.ManyToManyField("Bet", related_name="Placed_Bet")


class Event(models.Model):
    id = models.AutoField()
    id.primary_key = True
    description = models.CharField(max_length=150)
    prize = models.CharField(max_length=100)
    creator = models.ForeignKey("User", on_delete=models.CASCADE)
    event_time = models.DateTimeField()
    event_type = models.IntegerField(null=False)
    participants = models.ManyToManyField("Group", related_name="Participates")
    type = models.ForeignKey("EventTypes", on_delete=models.CASCADE)


class EventType(models.Model):
    id = models.AutoField()
    id.primary_key = True
    event_type_name = models.CharField(max_length=150)


class ItemType(models.Model):
    id = models.AutoField()
    id.primary_key = True
    item_type_name = models.CharField(max_length=150)
