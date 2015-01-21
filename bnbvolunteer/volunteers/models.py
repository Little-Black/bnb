from django.db import models
from django.db.models import signals
from django.contrib.auth.models import User
from datetime import datetime
from datetime import date
from random import random
from threading import Timer

#Userlog is now Activity!!! Userlog just here for reference.
# class Userlog(models.Model):
#     user = models.ForeignKey(User, default='')
#     date = models.CharField(max_length=200)
#     task = models.CharField(max_length=200)
#     hours = models.PositiveSmallIntegerField(default=0)
#     rate = models.PositiveSmallIntegerField(default=2)
#     voucherearned = models.PositiveSmallIntegerField(default=0)

class ActivityType(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Activity(models.Model):
    user = models.ForeignKey(User, default='', related_name='user')
    dateDone = models.DateField(default=date.today)
    dateEntered = models.DateTimeField(auto_now_add=True, blank=True)
    activityType = models.ForeignKey(ActivityType, null=True, default='')
    description = models.CharField(max_length=200)
    credits = models.PositiveSmallIntegerField(default=0)
    staff = models.ForeignKey(User, null=True, related_name='staff')

class Voucher(models.Model):
    code = models.CharField(max_length=200)
    credits = models.PositiveSmallIntegerField(default=0)
    redemptionActivity = models.ForeignKey(Activity, null=True, blank=True)

class VerificationRequest(models.Model):
    user = models.ForeignKey(User)
    code = models.CharField(max_length=20)
    actionType = models.CharField(max_length=100)
    isValid = models.BooleanField(default=True)
    creationTime = models.DateTimeField(auto_now_add=True)
    data = models.CharField(max_length=200, blank=True)
    
    def verify(self):
        if self.actionType == "register":
            self.user.is_active = True
            self.user.save()
            message = "Email successfully verified, account now active."
        elif self.actionType == "updateEmail":
            (self.user.email, self.user.profile.newEmail) = (self.user.profile.newEmail, "")
            self.user.save()
            message = "Email successfully updated."
        elif self.actionType == "resetPassword":
            self.user.set_password(self.data)
            self.user.save()
            message = "Password successfully reset."
        elif self.actionType == "deleteAcc":
            self.user.delete()
            message = "Email successfully verified, your account will be deleted."
        else:
            message = "Invalid action type."
        self._selfDestruct()
        return message
    
    def _selfDestruct(self, hasExpired=False):
        if self.isValid:
            if hasExpired:
                if self.actionType == "register":
                    self.user.delete()
            self.isValid = False
            self.delete()
    
    @classmethod
    def _generateLetterString(cls, length):
        def generateRandomChar():
            lowercaseFactor = (1 if random() >= 0.5 else 0)
            return chr(int(26*random())+32*lowercaseFactor+65)
        gString = ""
        for i in xrange(length):
            gString += generateRandomChar()
        if VerificationRequest.objects.filter(code=gString):
            return VerificationRequest._generateLetterString(length)
        else:
            return gString
    
    @classmethod
    def createVerificationRequest(cls, user, actionType, timeLimit=60*60*48, **kwargs):
        prevRequests = VerificationRequest.objects.filter(user=user)
        # at most 1 request for each type
        for prevRequest in prevRequests:
            if prevRequest.actionType == actionType:
                prevRequest._selfDestruct()
        request = VerificationRequest.objects.create(user=user, code=VerificationRequest._generateLetterString(20), actionType=actionType, **kwargs)
        Timer(timeLimit, request._selfDestruct, [True,]).start()
        return request
    
    def __unicode__(self):
        return "code="+self.code


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile")
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)
    newEmail = models.EmailField(blank=True) # holds unverified email address
    credit = models.PositiveSmallIntegerField(default=0)
    
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
    
    def __unicode__(self):
        return "user="+self.user.username

def createUserProfile(sender, instance, **kwargs):
    if not hasattr(instance, "profile"):
        UserProfile.objects.create(user=instance)

# Automatically create a profile after user info is saved, if one has not been created already
signals.post_save.connect(createUserProfile, sender=User)
