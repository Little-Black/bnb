from django.db import models
from django.contrib.auth.models import User

class Userlog(models.Model):
    user = models.ForeignKey(User, default='')
    date = models.CharField(max_length=200)
    task = models.CharField(max_length=200)
    hours = models.PositiveSmallIntegerField(default=0)
    rate = models.PositiveSmallIntegerField(default=2)
    voucherearned = models.PositiveSmallIntegerField(default=0)
