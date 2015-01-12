from django.shortcuts import render
from volunteers.models import *
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from userManagement import *
from django.contrib.auth.decorators import login_required

@login_required
def volunteerHome(request):
    try:
        user = request.user #authenticate(username='admin', password='adMIN')
        query_results = Userlog.objects.filter(user=user)
    except:
        print "Not logged in"
        query_results = []
    context = {'query_results': query_results}
    return render(request,'volunteers/volunteerHome.html',context)

@login_required
def volunteerStaffHome(request):
    try:
        user = request.user #authenticate(username='admin', password='adMIN')
        query_results = Userlog.objects.filter(user=user)
    except:
        print "Not logged in"
        query_results = []
    context = {'query_results': query_results}
    return render(request,'volunteers/volunteerStaffHome.html',context)

@login_required
def volunteerSubmit(request):
    try:
        user = request.user #authenticate(username='admin', password='adMIN')
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
    query_results = Userlog.objects.filter(user=user)
    context = {'query_results': query_results}
    return render(request,'volunteers/volunteerHome.html',context)

def userLogin(request):
    if request.method == "POST":
        (loginSuccessful, context) = loginByForm(request, LoginForm(request.POST))
        if loginSuccessful:
            if "next" in request.GET:
                redirect = request.GET["next"]
            else:
                if not request.user.has_perm('staff_status'):
                    redirect = reverse("volunteerHome")
                else: 
                    redirect = reverse("volunteerStaffHome")
            return HttpResponseRedirect(redirect)
        else:
            return render(request, "volunteers/login.html", context)
    else:
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse("volunteerHome"))
        else:
            return render(request, "volunteers/login.html", {"form": LoginForm()})

def userRegistration(request):
    if request.method == "POST":
        (registrationSuccessful, context) = registerByForm(request, RegistrationForm(request.POST))
        if registrationSuccessful:
            return HttpResponseRedirect(reverse('userLogin'))
        else:
            return render(request, "volunteers/register.html", context)
    else:
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse("volunteerHome"))
        else:
            return render(request, "volunteers/register.html", {"form": RegistrationForm})
