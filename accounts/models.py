from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime
from django.utils import timezone
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100, blank=True)
    lastname = models.CharField(max_length=100, blank=True)
    dob = models.DateField(blank=True)
    join_date = models.DateField(default=date.today())
    bio = models.CharField(max_length=200, blank=True)
    address = models.CharField(max_length=200, blank=True)
    profession = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.firstname


class FriendModel(models.Model):
    member = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    friend = models.ForeignKey(User, on_delete=models.CASCADE)
    added = models.BooleanField(default=False)
    sent_date = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return str(self.member)