from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from volunteers.models import *
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse


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

def showLoginPage(request):
    return render(request, "volunteers/login.html", {})

def userLogin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse('volunteerHome'))
        else:
            return render(request, "volunteers/login.html", {"message": "Account has been disabled. Please contact admin."})
    else:
        return render(request, "volunteers/login.html", {"message": "Invalid username or password."})
