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
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)
    
    def get(self, attr):
        if hasattr(self, attr):
            return getattr(self, attr)
        elif hasattr(self.user, attr):
            return getattr(self.user, attr)
        else:
            raise AttributeError("cannot find "+attr)
    
    def set(self, attr, value):
        if hasattr(self, attr):
            setattr(self, attr, value)
        elif hasattr(self.user, attr):
            setattr(self.user, attr, value)
        else:
            setattr(self, attr, value)