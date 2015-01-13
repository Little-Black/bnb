from django.db import models
from django.db.models import signals
from django.contrib.auth.models import User

#Userlog is now Activity!!! Userlog just here for reference.
# class Userlog(models.Model):
#     user = models.ForeignKey(User, default='')
#     date = models.CharField(max_length=200)
#     task = models.CharField(max_length=200)
#     hours = models.PositiveSmallIntegerField(default=0)
#     rate = models.PositiveSmallIntegerField(default=2)
#     voucherearned = models.PositiveSmallIntegerField(default=0)

class Activity(models.Model):
    user = models.ForeignKey(User, default='')
    dateDone = models.CharField(max_length=200)
    dateEntered = models.CharField(max_length=200)
    activityType = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    credits = models.PositiveSmallIntegerField(default=0)

class Voucher(models.Model):
    code = models.CharField(max_length=200)
    credits = models.PositiveSmallIntegerField(default=0)
    redemptionActivity = models.ForeignKey(Activity, default='')

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile")
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

def createUserProfile(sender, instance, **kwargs):
    if not hasattr(instance, "profile"):
        UserProfile.objects.create(user=instance)

# Automatically create a profile after user info is saved, if one has not been created already
signals.post_save.connect(createUserProfile, sender=User)
