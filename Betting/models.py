from datetime import timedelta

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from MoneyTalks.settings import MEDIA_PATH, STATIC_PATH


def validate_nonzero(value):
    if value < 1:
        raise ValidationError(
            _('Quantity %(value)s is not allowed'),
            params={'value': value},
        )


def invalidationTime(time):
    return timezone.now() + timedelta(minutes=15)


def image_directory(profile, filename):
    return STATIC_PATH + "/img/" + str(profile.user.id) + "/pp.png"


def event_image_directory(event_type, filename):
    return STATIC_PATH + "/img/event/" + str(event_type.id) + "/pp.png"


# Create your models here.
class Bet(models.Model):
    amount = models.PositiveSmallIntegerField(validators=[MaxValueValidator(1000000), validate_nonzero])
    item = models.CharField(max_length=100)
    event = models.ForeignKey("Event", on_delete=models.CASCADE)
    better = models.ForeignKey(User, on_delete=models.CASCADE)
    betting_on = models.ForeignKey("Group", on_delete=models.CASCADE)
    invalidation_time = models.DateTimeField(default=invalidationTime(15))

    @property
    def active(self) -> bool:
        return timezone.localtime() < self.invalidation_time

    @property
    def won(self) -> bool:
        return self.event.winner == self.betting_on

    @property
    def calculate_winnings(self) -> {(str, int)}:
        bets = Bet.objects.filter(evet=self.event_id).exclude(betting_on=self.betting_on)
        bet_list = {}
        for bet in bets:
            if bet in bet_list:
                bet_list[bet.item] += bet.amount
            else:
                bet_list[bet.item] = bet.amount
        return bets

    def __str__(self):
        return str(self.event) + "-bet " + str(self.id)


class Group(models.Model):
    group_name = models.CharField(max_length=20, null=True, blank=True, default="New Group")
    event_id = models.ForeignKey("Event", on_delete=models.CASCADE)
    member = models.ManyToManyField(User, related_name="Group_Members")
    group_bet_amount = models.PositiveSmallIntegerField(validators=[MaxValueValidator(1000000), validate_nonzero])
    group_bet = models.CharField(max_length=100)

    @property
    def uneven_betting(self) -> bool:
        groups = Group.objects.filter(event_id=self.event_id).exclude(pk=self.pk)
        for group in groups:
            if group.group_bet != self.group_bet:
                return True
        return False

    @property
    def calculate_winnings(self) -> {(str, int)}:
        groups = Group.objects.filter(event_id=self.event_id).exclude(pk=self.pk)
        bets = {}
        for group in groups:
            if group.group_bet in bets:
                bets[group.group_bet] += group.group_bet_amount
            else:
                bets[group.group_bet] = group.group_bet_amount
        return bets

    def __str__(self):
        return self.group_name


@receiver(post_save, sender=User)
def update_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # picture
    winner_speech = models.CharField(max_length=500, null=True, blank=True)
    picture = models.ImageField(upload_to=image_directory, default=MEDIA_PATH + "\default.png")

    @property
    def win_rate(self):
        groups = Group.objects.filter(member__in=[self.user.id])
        wins = 0
        lose = 0
        tie = 0
        for group in groups:
            if group.event_id.finalized:
                if not group.event_id.tie:
                    if group.event_id.winner == group:
                        wins += 1
                    else:
                        lose += 1
                else:
                    tie += 1
        return [wins, lose, tie]

    def __str__(self):
        return self.user.username


class EventType(models.Model):
    type = models.CharField(max_length=100)
    image = models.ImageField(upload_to=event_image_directory,
                              default=MEDIA_PATH + "\event\default.png")

    def __str__(self):
        return self.type


class Event(models.Model):
    description = models.CharField(max_length=150, null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    event_date = models.DateField()
    event_time = models.TimeField()
    event_type = models.ForeignKey("EventType", on_delete=models.CASCADE)
    tie = models.BooleanField(null=True, blank=True)
    winner = models.OneToOneField("Group", on_delete=models.CASCADE, null=True, blank=True)

    # tournament = models.ForeignKey("Tournament", on_delete=models.CASCADE, null=True, blank=True)

    @property
    def active(self) -> bool:
        if timezone.localdate() > self.event_date:
            return False
        elif timezone.localdate() == self.event_date and timezone.localtime().time() > self.event_time:
            return False
        return True

    @property
    def finalized(self) -> bool:
        if not self.active and self.winner is not None:
            return True
        elif not self.active and self.tie:
            return True
        else:
            return False

    def __str__(self):
        return str(self.id) + " " + self.description

# class Tournament(models.Model):
# description = models.CharField(max_length=150)
# amount = models.IntegerField()
# prize = models.CharField(max_length=100)
# time = models.DateTimeField()
