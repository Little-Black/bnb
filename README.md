Volunteer Credit System
===
Volunteer credit system is a Django application that allow non-profits to efficiently give credits to and manage volunteers.

# Usage
For development server:

1. run setup.py
2. type in "python manage.py runserver" in command line

# Features
- customizable for each site
- security against user abuse and attacks

# Requirements
- python 2.7
- Django 1.7
- django-simple-captcha (can be installed by "pip install django-simple-captcha")
- dj_static

# FAQ
Q: How do I create more superusers?

A: You can run "python manage.py createsuperuser" inside bnbvolunteer directory or use the admin interface.

Q: How can I change the email contents?

A: Edit bnbvolunteer/volunteers/emailTemplates.py. Note that this step requires basic python knowledge.