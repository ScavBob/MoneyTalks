from django.db import models
from django.http import HttpResponse
from django.db.models.functions import Now


# Create your models here.
class Bet(models.Model):
    id = models.AutoField()
    id.primary_key = True
    amount = models.PositiveSmallIntegerField()
    item = models.CharField(max_length=100)
    event = models.ForeignKey("Event", on_delete=models.CASCADE)
    betting_on = models.ForeignKey("Group", on_delete=models.CASCADE)
    creation_time = models.DateTimeField(Now())

    def __str__(self):
        return str(self.event) + "-bet " + str(self.id)


class Group(models.Model):
    id = models.AutoField()
    id.primary_key = True
    group_name = models.CharField(max_length=20, null=True, blank=True, default="New Group")
    event_id = models.ForeignKey("Event", on_delete=models.CASCADE)
    member = models.ManyToManyField("User", related_name="Group_Members")
    group_bet_amount = models.PositiveSmallIntegerField()
    group_bet = models.CharField(max_length=100)

    def __str__(self):
        return self.group_name


class User(models.Model):
    id = models.AutoField()
    id.primary_key = True
    # picture
    # win rate
    # old bets
    # current bets
    # password
    name = models.CharField(max_length=100)
    # password = models.CharField(max_length=100)
    # picture = models.ImageField()
    bets = models.ManyToManyField("Bet", related_name="Placed_Bet", blank=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    id = models.AutoField()
    id.primary_key = True
    description = models.CharField(max_length=150, null=True, blank=True)
    creator = models.ForeignKey("User", on_delete=models.CASCADE)
    event_time = models.DateTimeField()
    event_type = models.CharField(max_length=100)

    def __str__(self):
        return str(self.id) + " " + self.description
