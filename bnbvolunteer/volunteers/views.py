from django.shortcuts import render
from django.http.response import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from volunteers import userManagement
from volunteers.models import *
from volunteers.userManagement import *

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
def volunteerStaffHome(request):
    try:
        user = request.user #authenticate(username='admin', password='adMIN')
        query_results = Activity.objects.all()
    except:
        print "Not logged in"
        query_results = []
    context = {'query_results': query_results}
    return render(request,'volunteers/volunteerStaffHome.html',context)

@login_required
def volunteerStaffActivity(request):
    query_results = ActivityType.objects.all()
    context = {'query_results': query_results}
    return render(request, 'volunteers/volunteerStaffActivity.html', context)

@login_required
def volunteerStaffUserSearchResult(request):
    if request.POST['firstname'] == "":
        if request.POST['lastname'] == "":
            search_results = User.objects.all()
        else:
            search_results = User.objects.filter(last_name=request.POST['lastname'])
    else:
        search_results = User.objects.filter(last_name=request.POST['lastname']).filter(first_name=request.POST['firstname'])
    context = {'search_results': search_results}
    return render(request, 'volunteers/volunteerStaffSearchResults.html', context)

@login_required
def volunteerStaffUser(request):
    inform = ""
    userSearch_result = User.objects.get(username=request.GET['getuser'])
    search_results = Activity.objects.filter(user=userSearch_result)
    creditSum = 0
    for result in search_results:
        creditSum += result.credits
    if request.method == "POST":
        try:
            addLog = Activity(user=userSearch_result, description=request.POST['description'], credits=request.POST['credits'])
            if creditSum + int(addLog.credits) < 0:
                inform = "Do not have enough credits"
            else:
                addLog.save()
                search_results = Activity.objects.filter(user=userSearch_result)
                creditSum += int(addLog.credits)
        except:
            inform = "Please enter an integer in credits field."
    context = {'search_results': search_results, 'getuser':userSearch_result, 'inform': inform, 'totalCredit': creditSum}
    return render(request, 'volunteers/volunteerStaffUser.html', context)

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
        infoForm = EditProfileForm(request.POST)
        infoForm.process(request)
        pwForm = PasswordChangeForm(request.POST)
        if pwForm.isFilled(request):
            pwForm.process(request)
    else:
        infoForm = EditProfileForm(createUserContext(request.user))
        pwForm = PasswordChangeForm()
    return render(request, "volunteers/profile.html", {"infoForm": infoForm, "pwForm": pwForm})

def verify(request, code):
    verificationRequests = VerificationRequest.objects.filter(code=code)
    if verificationRequests:
        message = verificationRequests[0].verify()
        return HttpResponse(message)
    else:
        return HttpResponse("Invalid code.")

@login_required
def deleteAccount(request):
    userManagement.deleteAccount(request)
    return HttpResponseRedirect(reverse("editProfile"))

@login_required
def search(request):
    context = {}
    return render(request,'volunteers/search.html',context)

@login_required
def updateProfile(request):
    context = {}
    return render(request,'volunteers/updateProfile.html',context)

@login_required
def codeGenerator(request):
    context = {}
    return render(request,'volunteers/codeGenerator.html',context)
