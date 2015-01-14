# This file contains functions creating and modifying users.

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django import forms

from volunteers.models import *

class LoginForm(forms.Form):
    
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=30)
    
    """
    Attempt to login an user who filled out the login form.
    @param request: HTTPRequest
    @return True if and only if the user is successfully logged in
    """
    def process(self, request):
        loginSuccessful = False
        if self.is_valid():
            user = authenticate(username=self.cleaned_data["username"], password=self.cleaned_data["password"])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    loginSuccessful = True
                else:
                    messages.error(request, "Account has been disabled. Please contact admin.")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Please enter both username and password.")
        return loginSuccessful

class RegistrationForm(forms.Form):
    
    email = forms.EmailField()
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=30)
    password_confirmation = forms.CharField(widget=forms.PasswordInput(), max_length=30)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    address = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=30)

    """
    Attempt to register an user who filled out the registration form.
    @param request: HTTPRequest
    @return True if and only if the user is successfully registered
    """
    def process(self, request):
        registrationSuccessful = True
        if self.is_valid():
            if User.objects.filter(username=self.cleaned_data["username"]):
                messages.error(request, "This username is already taken.")
                registrationSuccessful = False
            if User.objects.filter(email=self.cleaned_data["email"]):
                messages.error(request, "This email is already connected to another account.")
                registrationSuccessful = False
            if self.cleaned_data["password"] != self.cleaned_data["password_confirmation"]:
                messages.error(request, "The passwords do not match.")
                registrationSuccessful = False
            if registrationSuccessful:
                user = User.objects.create_user(self.cleaned_data["username"],
                                                self.cleaned_data["email"],
                                                self.cleaned_data["password"],
                                                first_name=self.cleaned_data["first_name"],
                                                last_name=self.cleaned_data["last_name"])
                for attr in {"address", "phone"}:
                    user.profile.set(attr, self.cleaned_data[attr])
                user.is_active = False
                user.save()
                user.profile.save()
                vr = VerificationRequest.createVerificationRequest(user, actionType="register")
                # send verification mail to user (deactivated for the moment)
                emailMessage = "Hi " + user.first_name + ",\n\
                                Thank you for registering on BnB's volunteer system.\n\
                                Your username is " + user.username + ".\n\
                                You can activate your account at /verify/" + vr.code + "."
                #send_mail("Registration on BnB Volunteer System", emailMessage, "BnB Volunteer System", [user.email,])
                messages.success(request, "Registration successful. You should receive a verification mail in the inbox. (currently turned off) "+vr.code)
        else:
            registrationSuccessful = False
            for error in self.errors:
                messages.error(request, error + " is a required field.")
        return registrationSuccessful

class EditProfileForm(forms.Form):
    
    username = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    address = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=30)
    
    """
    Attempt to edit the account information of an user.
    @param request: HTTPRequest
    """
    def process(self, request):
        if self.is_valid():
            if request.user.email != self.cleaned_data["email"]:
                if User.objects.filter(email=self.cleaned_data["email"]):
                    messages.error(request, "This email is already connected to another account.")
                else:
                    messages.info(request, "A confirmation mail is sent to your new email address. (feature not yet implemented, ignore this)")
                    request.user.email = self.cleaned_data["email"]
            for attr in {"first_name", "last_name", "address", "phone"}:
                request.user.profile.set(attr, self.cleaned_data[attr])
            request.user.save()
            messages.success(request, "Account info successfully saved!")
        else:
            for error in self.errors:
                messages.error(request, error + " is a required field.")

def createUserContext(user):
    data = {}
    for attr in {"username", "email", "first_name", "last_name", "address", "phone"}:
        data[attr] = user.profile.get(attr)
    return data

class PasswordChangeForm(forms.Form):
    
    old_password = forms.CharField(widget=forms.PasswordInput(), max_length=30)
    new_password = forms.CharField(widget=forms.PasswordInput(), max_length=30)
    confirm_new_password = forms.CharField(widget=forms.PasswordInput(), max_length=30)
    
    def isFilled(self, request):
        fieldsFilled = dict()
        for field in {"old_password", "new_password", "confirm_new_password"}:
            try:
                fieldsFilled[field] = request.POST[field]
            except KeyError:
                return False
        return fieldsFilled["old_password"] or fieldsFilled["new_password"] or fieldsFilled["confirm_new_password"]
    
    """
    Attempt to change the password of the current user.
    @param request: HTTPRequest
    """    
    def process(self, request):
        if self.is_valid():
            if request.user.check_password(self.cleaned_data["old_password"]):
                if self.cleaned_data["new_password"] == self.cleaned_data["confirm_new_password"]:
                    messages.success(request, "Password successfully changed!")
                    request.user.set_password(self.cleaned_data["new_password"])
                    request.user.save()
                else:
                    messages.error(request, "The new passwords do not match.")
            else:
                messages.error(request, "The old password is incorrect.")
        else:
            for error in self.errors:
                messages.error(request, error + " is a required field.")

def deleteAccount(request):
    vr = VerificationRequest.createVerificationRequest(request.user, actionType="delete")
    messages.info(request, "A confirmation email is sent to your account. "+vr.code)