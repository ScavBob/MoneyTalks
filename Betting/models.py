from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponse
from django.db.models.functions import Now
from django.utils.translation import gettext_lazy as _
from MoneyTalks.settings import TIME_ZONE


def validate_nonzero(value):
    if value < 1:
        raise ValidationError(
            _('Quantity %(value)s is not allowed'),
            params={'value': value},
        )


def invalidationTime(time):
    return timezone.now() + timedelta(minutes=15)


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

    def __str__(self):
        return str(self.event) + "-bet " + str(self.id)


class Group(models.Model):
    group_name = models.CharField(max_length=20, null=True, blank=True, default="New Group")
    event_id = models.ForeignKey("Event", on_delete=models.CASCADE)
    member = models.ManyToManyField(User, related_name="Group_Members")
    group_bet_amount = models.PositiveSmallIntegerField(validators=[MaxValueValidator(1000000), validate_nonzero])
    group_bet = models.CharField(max_length=100)

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
    # win rate
    # old bets
    # current bets
    # password
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)

    # picture = models.ImageField()

    def __str__(self):
        return self.user.username


class Event(models.Model):
    description = models.CharField(max_length=150, null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    event_date = models.DateField()
    event_time = models.TimeField()
    event_type = models.CharField(max_length=100)
    # tournament = models.ForeignKey("Tournament", on_delete=models.CASCADE, null=True, blank=True)

    @property
    def active(self) -> bool:
        active = True
        if timezone.localdate() > self.event_date:
            active = False
        elif timezone.localdate() == self.event_date and timezone.localtime().time() > self.event_time:
            active = False
        return active

    def __str__(self):
        return str(self.id) + " " + self.description

# class Tournament(models.Model):
# description = models.CharField(max_length=150)
# amount = models.IntegerField()
# prize = models.CharField(max_length=100)
# time = models.DateTimeField()
