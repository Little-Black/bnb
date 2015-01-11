from django.db import models
from django.contrib.auth.models import User

class Userlog(models.Model):
    user = models.ForeignKey(User, default='')
    date = models.CharField(max_length=200)
    task = models.CharField(max_length=200)
    hours = models.PositiveSmallIntegerField(default=0)
    rate = models.PositiveSmallIntegerField(default=2)
    voucherearned = models.PositiveSmallIntegerField(default=0)

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    address = models.CharField(blank=True, max_length=100)
    phone = models.CharField(blank=True, max_length=30)