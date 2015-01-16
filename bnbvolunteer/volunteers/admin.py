from django.contrib import admin
from volunteers.models import *
from django.http import HttpResponse

admin.site.register(UserProfile)
admin.site.register(ActivityType)
admin.site.register(Activity)
admin.site.register(Voucher)

