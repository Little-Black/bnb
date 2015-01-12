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
        query_results = Userlog.objects.all()
    except:
        print "Not logged in"
        query_results = []
    context = {'query_results': query_results}
    return render(request,'volunteers/volunteerStaffHome.html',context)

@login_required
def volunteerStaffUserSearchResult(request):
    search_results = User.objects.filter(last_name=request.POST['lastname']).filter(first_name=request.POST['firstname'])
    context = {'search_results': search_results}
    return render(request, 'volunteers/volunteerStaffSearchResults.html', context)

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
        form = LoginForm(request.POST)
        if form.process(request):
            if "next" in request.GET:
                redirect = request.GET["next"]
            else:
                if not request.user.has_perm('staff_status'):
                    redirect = reverse("volunteerHome")
                else: 
                    redirect = reverse("volunteerStaffHome")
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
