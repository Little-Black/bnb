# Contains functions that generate email messages.

from django.core.mail import send_mail
from bnbvolunteer import settings

def _getVerificationURL(user, actionType):
    return settings.SITE_URL + "/verify/" + user.verificationrequest_set.get(actionType=actionType).code

def sendRegVerificationEmail(user):
    message = "Hi " + user.first_name + ",\n\
                Thank you for being interested in volunteering for Bikes not Bombs. Your username is " + user.username + ". You can activate your account at " + _getVerificationURL(user, "register") + "\n\
                The account will be deleted if it is not verified within the next 48 hours.\n\
                If you did not create the account, ignore this email."
    send_mail("Registration on BnB Volunteer System", message, settings.ORG_NAME, [user.email,])

def sendResetPasswordEmail(user):
    message = "Hi " + user.first_name + ",\n  You have requested to reset your password. Your password will be changed to " + user.verificationrequest_set.get(actionType="resetPassword").data + " after you access the link below:\n" + _getVerificationURL(user, "resetPassword") + "\nThis link is only valid for 48 hours. If you did not request a password change, ignore this email."
    send_mail("Resetting your BnB Volunteer System Password", message, settings.ORG_NAME, [user.email,])

def sendEmailUpdateEmail(user):
    message = "Hi " + user.first_name + ",\n\
                This email is designated as the new email address of " + user.username +". Confirm this change by visiting " + _getVerificationURL(user, "updateEmail") + "\n\
                The link is only valid for 48 hours.\n\
                Ignore this email if the account shown above does not belong to you."
    send_mail("Updating your BnB Volunteer System Email", message, settings.ORG_NAME, [user.profile.newEmail,])

def sendDeleteAccEmail(user):
    message = "Hi " + user.first_name + ",\n\
                I am sorry to hear that you want to delete your account on Bikes not Bombs volunteering system.\
                You can delete your account by accessing " + _getVerificationURL(user, "deleteAcc") + "\n\
                The link is only valid for 48 hours.\n\
                If you did not ask for your account to be deleted, ignore this email and change your password."
    send_mail("Deleting your BnB Volunteer Account", message, settings.ORG_NAME, [user.email,])