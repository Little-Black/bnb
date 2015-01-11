# This file contains functions creating and modifying users.

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django import forms

from volunteers.models import UserProfile

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=30)

"""
Attempt to login a user who filled out the login form.
@param request: HTTPRequest
@param form: LoginForm
@return (a,b) where:
            a = True if and only if the user is successfully logged in
            b = a dictionary, with key "form" containing the form and an optional key "message" containing an error message
"""
def loginByForm(request, form):
    loginSuccessful = False
    context = dict()
    if form.is_valid():
        user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password"])
        if user is not None:
            if user.is_active:
                login(request, user)
                loginSuccessful = True
            else:
                context["message"] = "Account has been disabled. Please contact admin."
        else:
            context["message"] = "Invalid username or password."
    else:
        context["message"] = "Please enter both username and password."
    context["form"] = form
    return (loginSuccessful, context)

class RegistrationForm(forms.Form):
    email = forms.EmailField()
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=30)
    password_confirmation = forms.CharField(widget=forms.PasswordInput(), max_length=30)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    address = forms.CharField(required=False)
    phone = forms.CharField(required=False)

"""
Attempt to register a user who filled out the registration form.
@param request: HTTPRequest
@param form: RegistrationForm
@return (a,b) where:
            a = True if and only if the user is successfully registered
            b = a dictionary, with key "form" containing the form and "messages" containing error messages
"""
def registerByForm(request, form):
    registrationSuccessful = True
    messages = set()
    if form.is_valid():
        if User.objects.filter(username=form.cleaned_data["username"]):
            messages.add("This username is already taken.")
            registrationSuccessful = False
        if User.objects.filter(email=form.cleaned_data["email"]):
            messages.add("This email is already taken.")
            registrationSuccessful = False
        if form.cleaned_data["password"] != form.cleaned_data["password_confirmation"]:
            messages.add("The passwords do not match.")
            registrationSuccessful = False
        if registrationSuccessful:
            user = User.objects.create_user(form.cleaned_data["username"],
                                            form.cleaned_data["email"],
                                            form.cleaned_data["password"],
                                            first_name=form.cleaned_data["first_name"],
                                            last_name=form.cleaned_data["last_name"])
            userProfile = UserProfile(user=user, address=form.cleaned_data["address"], phone=form.cleaned_data["phone"])
            userProfile.save()
    else:
        registrationSuccessful = False
        for error in form.errors:
            messages.add(error + " is a required field.")
    return (registrationSuccessful, {"form": form, "messages": messages})