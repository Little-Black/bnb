from django.shortcuts import render
from volunteers.models import *
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from userManagement import *

@login_required
def volunteerHome(request):
    try:
        user = request.user #authenticate(username='admin', password='adMIN')
        query_results = Activity.objects.filter(user=user)
        total_credits = 0
        for log in query_results:
            total_credits += log.credits
    except:
        print "Not logged in"
        query_results = []
    context = {'query_results': query_results,'total_credits':total_credits}
    return render(request,'volunteers/volunteerHome.html',context)

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
    activity = Activity(user=user,dateDone=date,description=task,credits=totalearned) #request.user
    try: 
        activity.save()
    except:
        print "ERROR"
    # return render(RequestContext(request),'volunteerHome.html')
    query_results = Activity.objects.filter(user=user)
    total_credits = 0
    for log in query_results:
        total_credits += log.credits
    context = {'query_results': query_results,'total_credits':total_credits}
    return render(request,'volunteers/volunteerHome.html',context)

def userLogin(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.process(request):
            redirect = request.GET["next"] if "next" in request.GET else reverse("volunteerHome")
            return HttpResponseRedirect(redirect)
        else:
            return render(request, "volunteers/login.html", {"form": form})
    else:
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse("volunteerHome"))
        else:
            return render(request, "volunteers/login.html", {"form": LoginForm()})

def userRegistration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.process(request):
            return HttpResponseRedirect(reverse('userLogin'))
        else:
            return render(request, "volunteers/register.html", {"form": form})
    else:
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse("volunteerHome"))
        else:
            return render(request, "volunteers/register.html", {"form": RegistrationForm()})

@login_required
def editProfile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST)
        form.process(request)
    else:
        form = EditProfileForm(createUserContext(request.user))
    return render(request, "volunteers/profile.html", {"form": form})

@login_required
def search(request):
    context = {}
    return render(request,'volunteers/search.html',context)

@login_required
def updateProfile(request):
    context = {}
    return render(request,'volunteers/updateProfile.html',context)