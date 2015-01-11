from django.shortcuts import render
from volunteers.models import *
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from userManagement import *

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

def userLogin(request):
    if request.method == "POST":
        (loginSuccessful, context) = loginByForm(request, LoginForm(request.POST))
        if loginSuccessful:
            return HttpResponseRedirect(reverse('volunteerHome'))
        else:
            return render(request, "volunteers/login.html", context)
    else:
        return render(request, "volunteers/login.html", {"form": LoginForm()})

def userRegistration(request):
    if request.method == "POST":
        (registrationSuccessful, context) = registerByForm(request, RegistrationForm(request.POST))
        if registrationSuccessful:
            return HttpResponseRedirect(reverse('volunteerHome'))
        else:
            return render(request, "volunteers/register.html", context)
    else:
        return render(request, "volunteers/register.html", {"form": RegistrationForm})