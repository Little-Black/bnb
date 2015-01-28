# This file contains functions creating and modifying users.

from django import forms
from django.core.cache import cache
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from captcha.fields import CaptchaField
from volunteers.models import VerificationRequest
from volunteers.emailTemplates import sendRegVerificationEmail, sendResetPasswordEmail, sendEmailUpdateEmail, sendDeleteAccEmail

from random import randint
from re import search, sub

def _isValidPassword(pwString):
    return len(pwString) >= 6

def _createErrorMessage(error):
    if error == "captcha":
        return "Invalid captcha response"
    else:
        return "Missing required field: %s" % sub("_", " ", error)

class LoginForm(forms.Form):
    
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=30)
    captcha = CaptchaField()
    
    @staticmethod
    def _cacheKey(request):
        return (request.META["REMOTE_ADDR"], "login")
    
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
                    messages.error(request, "You must verify your email address first.")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            if "username" in request.POST and request.POST["username"] and "password" in request.POST and request.POST["password"]:
                messages.error(request, "Invalid captcha response.")
            else:
                messages.error(request, "Please enter both username and password.")
        if not loginSuccessful:
            pass
            cache.set(LoginForm._cacheKey(request), cache.get(LoginForm._cacheKey(request),0)+1, 300)
        return loginSuccessful
    
    @classmethod
    def createLoginForm(cls, request, data=None):
        form = LoginForm(data)
        form.fields["captcha"].required = cache.get(LoginForm._cacheKey(request),0) >= 5
        return form
    
class RegistrationForm(forms.Form):
    
    email = forms.EmailField()
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=30)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), max_length=30)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    address = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=30)
    captcha = CaptchaField()

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
            if search("[^A-Za-z0-9_]", self.cleaned_data["username"]):
                messages.error(request, "Username can only contain alphanumeric characters and underscores.")
                registrationSuccessful = False
            if User.objects.filter(email=self.cleaned_data["email"]):
                messages.error(request, "This email is already connected to another account.")
                registrationSuccessful = False
            if self.cleaned_data["password"] != self.cleaned_data["confirm_password"]:
                messages.error(request, "The passwords do not match.")
                registrationSuccessful = False
            if not _isValidPassword(self.cleaned_data["password"]):
                messages.error(request, "The password must be at least 6 characters long.")
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
                sendRegVerificationEmail(user, vr)
                messages.success(request, "Registration successful. You should receive a verification mail in the inbox.")
        else:
            registrationSuccessful = False
            for error in self.errors:
                messages.error(request, _createErrorMessage(error))
        return registrationSuccessful

class EditProfileForm(forms.Form):
    
    username = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    address = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=30)
    
    @staticmethod
    def createUserContext(user):
        data = {}
        for attr in {"username", "email", "first_name", "last_name", "address", "phone"}:
            data[attr] = user.profile.get(attr)
        return data
    
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
                    messages.info(request, "A confirmation mail is sent to your new email address.")
                    request.user.profile.newEmail = self.cleaned_data["email"]
                    request.user.profile.save()
                    vr = VerificationRequest.createVerificationRequest(request.user, actionType="updateEmail")
                    sendEmailUpdateEmail(request.user, vr)
            for attr in {"first_name", "last_name", "address", "phone"}:
                request.user.profile.set(attr, self.cleaned_data[attr])
            request.user.save()
            request.user.profile.save()
            messages.success(request, "Account info successfully saved!")
        else:
            for error in self.errors:
                messages.error(request, _createErrorMessage(error))

class PasswordChangeForm(forms.Form):
    
    old_password = forms.CharField(widget=forms.PasswordInput(), max_length=30)
    new_password = forms.CharField(widget=forms.PasswordInput(), max_length=30)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), max_length=30)
    
    def isFilled(self, request):
        fieldsFilled = dict()
        for field in {"old_password", "new_password", "confirm_new_password"}:
            try:
                fieldsFilled[field] = request.POST[field]
            except KeyError:
                return False
        return fieldsFilled["old_password"] or fieldsFilled["new_password"] or fieldsFilled["confirm_password"]
    
    """
    Attempt to change the password of the current user.
    @param request: HTTPRequest
    """
    def process(self, request):
        if self.is_valid():
            if request.user.check_password(self.cleaned_data["old_password"]):
                if not _isValidPassword(self.cleaned_data["new_password"]):
                    messages.error(request, "The new password must be at least 6 characters long.")
                else:
                    if self.cleaned_data["new_password"] == self.cleaned_data["confirm_password"]:
                        messages.success(request, "Password successfully changed!")
                        request.user.set_password(self.cleaned_data["new_password"])
                        request.user.save()
                    else:
                        messages.error(request, "The new passwords do not match.")
            else:
                messages.error(request, "The old password is incorrect.")
        else:
            for error in self.errors:
                messages.error(request, _createErrorMessage(error))

class RequestPasswordResetForm(forms.Form):
    
    email = forms.EmailField()
    username = forms.CharField(max_length=30)
    
    @staticmethod
    def _generatePassword():
        def generateRandomChar():
            randNumber = randint(0,61)
            if randNumber < 10:
                return chr(48+randNumber)
            else:
                return chr(65+(randNumber-10)/26*32+(randNumber-10)%26)
        gString = ""
        for i in xrange(8):
            gString += generateRandomChar()
        return gString
    
    def process(self, request):
        if self.is_valid():
            try:
                user = User.objects.get(email=self.cleaned_data["email"], username=self.cleaned_data["username"])
                vr = VerificationRequest.createVerificationRequest(user, actionType="resetPassword", data=RequestPasswordResetForm._generatePassword())
                sendResetPasswordEmail(user, vr)
                messages.success(request, "A confirmation email is sent to your inbox.")
            except User.DoesNotExist:
                messages.error(request, "Cannot find an user with given information.")
        else:
            for error in self.errors:
                messages.error(request, error + " is a required field.")

def userDeleteAccount(request):
    messages.info(request, "A confirmation email is sent to your account.")
    vr = VerificationRequest.createVerificationRequest(request.user, actionType="deleteAcc")
    sendDeleteAccEmail(request.user, vr)