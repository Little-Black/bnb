# Contains functions that generate email messages.

from django.core.mail import send_mail
from bnbvolunteer import settings

def _addHeaderAndSig(user, content):
    return "Hi %s,\n\n" % user.first_name + content + "\n\n%s" % settings.ORG_NAME

def sendRegVerificationEmail(user, vr):
    content = "Thank you for being interested in volunteering for %s." % settings.ORG_NAME +\
                "Your username is %s." % user.username +\
                "You can activate your account at\n" + vr.getURL() +"\n" +\
                "The account may be deleted if it is not verified within 48 hours.\n" +\
                "If you did not create the account, ignore this email."
    message = _addHeaderAndSig(user, content)
    send_mail("%s Volunteering Registration" % settings.ORG_NAME_SHORT, message, settings.ORG_NAME, [user.email,])

def sendResetPasswordEmail(user, vr):
    content = "You requested a password reset on %s Volunteering " % settings.ORG_NAME +\
                "and your password will be changed to %s after your access the link below:\n" % vr.data +\
                vr.getURL() + "\n" +\
                "This link is only guaranteed to work for 48 hours.\n" +\
                "If you did not request a password change, ignore this email."
    message = _addHeaderAndSig(user, content)
    send_mail("%s Volunteering Password Reset" % settings.ORG_NAME_SHORT, message, settings.ORG_NAME, [user.email,])

def sendEmailUpdateEmail(user, vr):
    content = "This email is designated as the new email address of %s  on %s Volunteering. " % (user.username, settings.ORG_NAME) +\
                "Confirm this change by accessing the link below:\n" +\
                vr.getURL() + "\n" +\
                "This link is only guaranteed to work for 48 hours.\n" +\
                "If you do not own this account, ignore this email."
    message = _addHeaderAndSig(user, content)
    send_mail("%s Volunteering Email Update" % settings.ORG_NAME_SHORT, message, settings.ORG_NAME, [user.profile.newEmail,])

def sendDeleteAccEmail(user, vr):
    content = "I am sorry to hear that you wish to delete your account on %s Volunteering. " % settings.ORG_NAME +\
                "Your account will be deleted when you access the link below:\n" +\
                vr.getURL() + "\n" +\
                "This link is only guaranteed to work for 48 hours.\n" +\
                "If you did not request to delete this account, ignore this email and change your password."
    message = _addHeaderAndSig(user, content)
    send_mail("%s Volunteering Account Deletion" % settings.ORG_NAME_SHORT, message, settings.ORG_NAME, [user.email,])