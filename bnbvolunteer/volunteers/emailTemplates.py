# Contains functions that generate email messages.

from django.core.mail import send_mail

def sendRegVerificationEmail(user):
    message = "Hi " + user.first_name + ",\n\
                Thank you for being interested in volunteering for Bikes not Bombs. Your username is " + user.username + ".\n\
                You can activate your account at http://localhost:8000/verify/" + user.verificationrequest_set.all()[0].code + "\n\
                The account will be deleted if it is not verified within the next 48 hours.\n\
                If you did not create the account, ignore this email."
    send_mail("Registration on BnB Volunteer System", message, "BnB Volunteer System", [user.email,])

def sendDeleteAccEmail(user):
    message = "Hi " + user.first_name + ",\n\
                I am sorry to hear that you want to delete your account on Bikes not Bombs volunteering system.\
                You can delete your account by accessing http://localhost:8000/verify" + user.verificationrequest_set.all()[0].code + "\n\
                The link is only valid for 48 hours.\n\
                If you did not ask for your account to be deleted, ignore this email and change your password."
    send_mail("Deleting your BnB Volunteer Account", message, "BnB Volunteer System", [user.email,])