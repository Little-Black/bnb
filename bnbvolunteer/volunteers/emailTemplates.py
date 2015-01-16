# Contains functions that generate email messages.

from django.core.mail import send_mail

def _generateVerificationURL(user):
    return "http://localhost:8000/verify/" + user.verificationrequest_set.all()[0].code

def sendRegVerificationEmail(user):
    message = "Hi " + user.first_name + ",\n\
                Thank you for being interested in volunteering for Bikes not Bombs. Your username is " + user.username + ". You can activate your account at " + _generateVerificationURL(user) + "\n\
                The account will be deleted if it is not verified within the next 48 hours.\n\
                If you did not create the account, ignore this email."
    send_mail("Registration on BnB Volunteer System", message, "BnB Volunteer System", [user.email,])

def sendEmailUpdateEmail(user):
    message = "Hi " + user.first_name + ",\n\
                This email is designated as the new email address of " + user.username +". Confirm this change by visiting " + _generateVerificationURL(user) + "\n\
                The link is only valid for 48 hours.\n\
                Ignore this email if the account shown above does not belong to you."
    send_mail("Registration on BnB Volunteer System", message, "BnB Volunteer System", [user.profile.newEmail,])

def sendDeleteAccEmail(user):
    message = "Hi " + user.first_name + ",\n\
                I am sorry to hear that you want to delete your account on Bikes not Bombs volunteering system.\
                You can delete your account by accessing http://localhost:8000/verify" + user.verificationrequest_set.all()[0].code + "\n\
                The link is only valid for 48 hours.\n\
                If you did not ask for your account to be deleted, ignore this email and change your password."
    send_mail("Deleting your BnB Volunteer Account", message, "BnB Volunteer System", [user.email,])