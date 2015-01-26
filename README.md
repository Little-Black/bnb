Volunteer Credit System
===
Volunteer credit system is a Django application that allow non-profits to efficiently give credits to and manage volunteers.

# Usage
For development server:

1. run setup.py

2. type in "python manage.py runserver" in command line

To change the info provided in setup.py, run the script again and restart the server.

# Features
- customizable for each site
- security against user abuse and attacks

# Requirements
- Django 1.7
- django-simple-captcha
- dj_static

# Common Issues
Issue: encounter "cannot find vcs_cache_table" when running a development server
Solution: run "python manage.py createcachetable" before starting the server