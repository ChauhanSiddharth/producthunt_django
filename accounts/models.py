from django.db import models
from django.contrib.auth.models import User
from datetime import date
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
