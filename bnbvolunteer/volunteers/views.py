from django.shortcuts import render
from django.http.response import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from random import randint

from volunteers import userManagement
from volunteers.models import *
from volunteers.userManagement import *

@login_required
def volunteerHome(request):
    try:
        user = request.user #authenticate(username='admin', password='adMIN')
        context = getVolunteerPageContext(request,user)
    except:
        print "Not logged in"
        context = {'query_results': [],'total_credits':0,'type_choices':[]}
    return render(request,'volunteers/volunteerHome.html',context)

@login_required
def volunteerSubmit(request):
    try:
        user = request.user #authenticate(username='admin', password='adMIN')
    except:
        print "ERROR UGHHH"
    date = request.POST['date']
    print request.POST['activityType']
    try:
        activityType = ActivityType.objects.filter(name=request.POST['activityType'])[0]
    except:
        activityType1 = ActivityType(name="Edit me out later")
        activityType2 = ActivityType(name="Views.py somewhere")
        activityType1.save()
        activityType2.save()
        activityType = ActivityType.objects.filter(name=request.POST['activityType'])[0]
    # activityType.save()
    description = request.POST['description']
    earned = request.POST.getlist('myInputs')
    totalearned = 0
    for input in earned:
        totalearned += int(input)
    print date
    storedate = date[6:10]+'-'+date[0:2]+'-'+date[3:5]
    print storedate
    activity = Activity(user=user,dateDone=storedate,activityType = activityType, description=description,credits=totalearned) #request.user
    # try: 
    activity.save()
    # except:
    #     print "ERROR"

    context = getVolunteerPageContext(request,user)
    return render(request,'volunteers/volunteerHome.html',context)

def getVolunteerPageContext(request,user):
    query_results = Activity.objects.filter(user=user)
    total_credits = 0
    for log in query_results:
        total_credits += log.credits
    type_choices = ActivityType.objects.values_list('name', flat=True)
    # jq = ActivityType.objects.exclude(id__in=activities)
    # type_choices = jq.values_list('name', flat=True)
    if len(type_choices) == 0:
        type_choices = ["Edit me out later","Views.py somewhere"]
    context = {'query_results': query_results,'total_credits':total_credits,'type_choices':type_choices}
    return context


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

    # try:
    #     user = request.user #authenticate(username='admin', password='adMIN')
    #     context = getVolunteerPageContext(request,user)
    # except:
    #     print "Not logged in"
    #     context = {'query_results': [],'total_credits':0,'type_choices':[]}
    # return render(request,'volunteers/volunteerHome.html',context)

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

#Returns a random integer between min (inclusive) to max (inclusive)
def getRandomInt(min, max):
    return randint(min, max)

alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"];
#Returns a string of a single random capitalized letter of the alphabet 
def getRandomLetter():
    letterInt = getRandomInt(0,25)
    return alphabet[letterInt]

#Generates an 8-digit-long random code that alternates between capital letters and numbers 1-9
def generateCode():
    code = ""
    for i in range(0,8):
        if (i%2 == 0):
            letter = getRandomLetter()
            code += str(letter)
        else:
            integer = getRandomInt(1,9)
            code += str(integer)
    return code

@login_required
def generateCodes(request):
    generatedVouchers = []
    for counter in range(1,16):
        voucherInfo = request.POST.getlist("myInputs"+str(counter))
        print "Let's a go! For the "+str(counter)+"th time!"
        print "voucherInfo:"+str(voucherInfo)
        if voucherInfo == []:
            print "We've reached the endddddd"
            break
        points = voucherInfo[0]
        quantity = voucherInfo[1]
        if (points == "" or quantity == ""):
            print "You left a field blank yo.."
            #TODO: redirect them to the same page with an error message telling the user to try again TODO

        for i in range(int(quantity)):
            newCode = generateCode()
            while (Voucher.objects.filter(code=newCode).exists()):
                newCode = generateCode()

            voucher = Voucher(code=newCode, credits=int(points))
            voucher.save()
            generatedVouchers.append(voucher)
    context = {'generatedVouchers': generatedVouchers}
    return render(request,'volunteers/viewGeneratedCodes.html',context)

@login_required
def viewGeneratedCodes(request):
    generatedVouchers = request.generatedVouchers
    context = {'generatedVouchers': generatedVouchers}
    return render(request,'volunteers/viewGeneratedCodes.html',context)
