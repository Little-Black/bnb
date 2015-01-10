from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate
from volunteers.models import *


def volunteerHome(request):
    csrfContext = RequestContext(request)
    print "um"
    return render(request,'volunteerHome.html')

def volunteerSubmit(request):
    print "hey"
    try:
        user = authenticate(username='admin', password='adMIN')
    except:
        print "ERROR UGHHH"
    date = request.POST['date']
    task = request.POST['task']
    hours = request.POST['hours']
    rate = request.POST['rate']
    earned = request.POST['earned']
    userlog = Userlog(user=user,date=date,task=task,hours=hours,rate=rate,voucherearned=earned) #request.user
    try: 
        userlog.save()
    except:
        print "ERROR"
    # return render(RequestContext(request),'volunteerHome.html')
    csrfContext = RequestContext(request)
    return render(request,'volunteerHome.html')


