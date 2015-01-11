from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate
from volunteers.models import *


def volunteerHome(request):
    query_results = Userlog.objects.all()
    context = {'query_results': query_results}
    return render(request,'volunteers/volunteerHome.html',context)

def volunteerSubmit(request):
    try:
        user = authenticate(username='admin', password='adMIN')
    except:
        print "ERROR UGHHH"
    date = request.POST['date']
    task = request.POST['task']
    hours = request.POST['hours']
    rate = request.POST['rate']
    print request.POST.getlist('myInputs')
    earned = request.POST.getlist('myInputs')
    totalearned = 0
    for input in earned:
        totalearned += int(input)
        print totalearned
    userlog = Userlog(user=user,date=date,task=task,hours=hours,rate=rate,voucherearned=totalearned) #request.user
    try: 
        userlog.save()
    except:
        print "ERROR"
    # return render(RequestContext(request),'volunteerHome.html')
    query_results = Userlog.objects.all()
    context = {'query_results': query_results}
    return render(request,'volunteers/volunteerHome.html',context)


