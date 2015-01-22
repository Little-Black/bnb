from django.shortcuts import render
from django.http.response import HttpResponseRedirect, HttpResponse
#from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.safestring import mark_safe

from bnbvolunteer import settings
from volunteers import userManagement
from volunteers.models import *
from volunteers.userManagement import *

from random import randint
from datetime import date
from datetime import datetime

import csv

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
    print earned
    totalearned = 0
    invalid = []
    invalid_boolean = "False"
    valid_vouchers = Voucher.objects.exclude(redemptionActivity__isnull=False)
    # print Voucher.objects.all()[1].redemptionActivity.description
    print "valid: " + str(valid_vouchers)
    vouchers_used = []
    for voucher_code in earned: #input
        voucher_set = valid_vouchers.filter(code = voucher_code.encode('utf8'))
        print voucher_code.encode('utf8')
        if len(voucher_set)==1:
            # print voucher
            voucher = voucher_set[0]
            totalearned+=voucher.credits
            vouchers_used.append(voucher)
            print "VALID!"
        elif len(voucher_set)==0:
            invalid.append((voucher_code.encode('utf8')))
            invalid_boolean = "True"
        else: 
            return HttpResponse("Error: Multiple vouchers exist for that code")
    storedate = date[6:10]+'-'+date[0:2]+'-'+date[3:5] #reformat the date :/
    activity = Activity(user=user,dateDone=storedate,activityType = activityType, description=description,credits=totalearned) #request.user
    # try: 
    if len(invalid) == 0:
        activity.save()
    # except:
    #     print "ERROR"
    for voucher in vouchers_used:
        voucher.redemptionActivity = activity
        voucher.save()

    context = getVolunteerPageContext(request,user)
    # return HttpResponse("Hi there!")
    context['invalid_vouchers']=mark_safe(invalid)
    context['invalid_boolean']=invalid_boolean
    print invalid_boolean
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

@user_passes_test(lambda user: user.is_staff)
def volunteerStaffHome(request):
    Logs = Activity.objects.all()
    try:
        user = request.user #authenticate(username='admin', password='adMIN')
    except:
        print "Not logged in"
    context = {'Logs': Logs}
    return render(request,'volunteers/volunteerStaffHome.html',context)

    # try:
    #     user = request.user #authenticate(username='admin', password='adMIN')
    #     context = getVolunteerPageContext(request,user)
    # except:
    #     print "Not logged in"
    #     context = {'query_results': [],'total_credits':0,'type_choices':[]}
    # return render(request,'volunteers/volunteerHome.html',context)

@user_passes_test(lambda user: user.is_staff)
def volunteerStaffLog(request):
    type_choices = ActivityType.objects.all()
    Logs = Activity.objects.all().order_by('-dateEntered')
    if request.method == "POST":
        try:
            Logs = Logs.exclude(dateDone__gt = request.POST['dateDoneUp'])
        except:
            Logs = Logs
        try:
            Logs = Logs.filter(dateDone__gte = request.POST['dateDoneDown'])
        except:
            Logs = Logs
        if not request.POST['activityType'] == "All":
            activityType = ActivityType.objects.get(name=request.POST['activityType'])
            Logs = Logs.filter(activityType = activityType)
        try:
            Logs = Logs.filter(credits__gte = request.POST['creditsDown'])
        except:
            Logs = Logs
        try:
            Logs = Logs.exclude(credits__gt = request.POST['creditsUp'])
        except:
            Logs = Logs
        Logs = Logs.order_by('-dateEntered')
        context = {'Logs': Logs, 'dateDoneUp': request.POST['dateDoneUp'], 'dateDoneDown': request.POST['dateDoneDown'], 'type_choices': type_choices, 'typeSelected': request.POST['activityType'], 'creditsDown': request.POST['creditsDown'], 'creditsUp': request.POST['creditsUp']}
    else:
        context = {'Logs': Logs, 'dateDoneUp': "", 'dateDoneDown': "", 'type_choices': type_choices, 'typeSelected': "All", 'creditsDown': "", 'creditsUp': ""}
    return render(request, 'volunteers/volunteerStaffLog.html', context)


@login_required
def volunteerStaffActivity(request):
    if request.method == "POST":
        if not request.POST['activityName'] == "":
            ActivityType(name=request.POST['activityName']).save()
    if 'delete' in request.GET:
        ActivityType.objects.get(id=request.GET['delete']).delete()
        return HttpResponseRedirect(reverse("volunteerStaffActivity"))
    query_results = ActivityType.objects.all()
    context = {'query_results': query_results}
    return render(request, 'volunteers/volunteerStaffActivity.html', context)

@login_required
def volunteerStaffUserSearchResult(request):
    inform = ""
    if request.method == "GET":
        search_results = User.objects.all() 
    else:
        if 'lastname' in request.POST.keys():
            if request.POST['lastname'] != "":    
                search_results = User.objects.filter(last_name=request.POST['lastname'])
            else:
                search_results = User.objects.all()
            try:
                search_results = search_results.filter(profile__credit__gte = request.POST['creditsDown'])
            except:
                search_results = search_results
            try:
                search_results = search_results.exclude(profile__credit__gt = request.POST['creditsUp'])
            except:
                search_results = search_results
            try:
                b = int(request.POST['phone']) + 1
                phone = request.POST['phone']
                search_results = search_results.filter(profile__phone = request.POST['phone'])
            except:
                search_results = search_results
                phone = ""
            try:
                if not request.POST['email'] == "":
                    search_results = search_results.filter(email = request.POST['email'])
            except:
                    search_results = search_results
            context = {'search_results': search_results, 'creditsDown': request.POST['creditsDown'], 'creditsUp': request.POST['creditsUp'], 'phone': phone, 'email': request.POST['email']}
            return render(request, 'volunteers/volunteerStaffSearchResults.html', context)
        else:
            search_results = User.objects.all()
            try:  
                s = 1 + int(request.POST['credits'])
                for user in search_results:
                    if user.username in request.POST.keys():
                        if request.POST[user.username]:
                            addLog = Activity(user=user,  description=request.POST['description'], credits=request.POST['credits'], staff=request.user)
                            if int(request.POST['credits']) + user.profile.credit >= 0:
                                addLog.save();
                                user.profile.credit += int(request.POST['credits'])
                                user.profile.save()
                            else:
                                inform += user.username + ', '
            except:
                inform = "Please type an integer in credits."
                context = {'search_results': search_results,  'inform': inform}
                return render(request, 'volunteers/volunteerStaffSearchResults.html', context)
    if not inform == "":
        inform = "No enough credits for " + inform[:-2] +"!" 
    context = {'search_results': search_results,  'inform': inform}
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
            addLog = Activity(user=userSearch_result,  description=request.POST['description'], credits=request.POST['credits'], staff=request.user)
            if creditSum + int(addLog.credits) < 0:
                inform = "Do not have enough credits"
            else:
                addLog.save()
                search_results = Activity.objects.filter(user=userSearch_result)
                creditSum += int(addLog.credits)
        except:
            inform = "Please type an integer in credits."
    userSearch_result.profile.credit = creditSum
    userSearch_result.profile.save()
    context = {'search_results': search_results, 'getuser':userSearch_result, 'inform': inform}
    return render(request, 'volunteers/volunteerStaffUser.html', context)

def userLogin(request):
    def redirect():
        if "next" in request.GET:
            return request.GET["next"]
        else:
            return reverse("volunteerStaffHome") if request.user.has_perm("staff_status") else reverse("volunteerHome")
    
    if request.method == "POST":
        form = LoginForm.createLoginForm(request, request.POST)
        if form.process(request):
            return HttpResponseRedirect(redirect())
    else:
        if request.user.is_authenticated():
            return HttpResponseRedirect(redirect())
        else:
            form = LoginForm.createLoginForm(request)
    return render(request, "volunteers/login.html", {"form": form})

def userLogout(request):
    logout(request)
    return HttpResponseRedirect(reverse("userLogin"))

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

def forgetPassword(request):
    if request.method == "POST":
        form = RequestPasswordResetForm(request.POST)
        if form.process(request):
            return HttpResponseRedirect(reverse('userLogin'))
        else:
            return render(request, "volunteers/forgetPassword.html", {"form": form})
    else:
        return render(request, "volunteers/forgetPassword.html", {"form": RequestPasswordResetForm()})

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
    returnPage = "volunteerHome"
    if request.user.has_perm("staff_status"):
        returnPage = "volunteerStaffHome"
    return render(request, "volunteers/profile.html", {"infoForm": infoForm, "pwForm": pwForm, "returnPage": returnPage})

def verify(request, code):
    cacheKey = (request.META["REMOTE_ADDR"], "verify")
    #if cache.get(cacheKey, 0) >= 5:
    #    return HttpResponse("You have entered too many invalid codes. Try again later.")
    else:
        try:
            verificationRequests = VerificationRequest.objects.get(code=code)
            message = verificationRequests.verify()
            return HttpResponse(message)
        except VerificationRequest.DoesNotExist:
            #cache.set(cacheKey, cache.get(cacheKey, 0)+1)
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

@user_passes_test(lambda user: user.is_staff)
def codeGenerator(request):
    query_results = Voucher.objects.all()
    if request.method == 'POST':
        if "isRedemed" in request.POST.keys():
            try:
                query_results = query_results.filter(generateDate__gte = request.POST['dateDown'])
            except:
                query_results = query_results
            try:
                query_results = query_results.exclude(generateDate__gt = request.POST['dateUp'])
            except:
                query_results = query_results
            try:
                query_results = query_results.filter(credits__gte = request.POST['creditsDown'])
            except:
                query_results = query_results
            try:
                query_results = query_results.exclude(credits__gt = request.POST['creditsUp'])
            except:
                query_results = query_results
            if request.POST['isRedemed'] == "Yes":
                query_results = query_results.exclude(redemptionActivity__isnull = True )
            if request.POST['isRedemed'] == "No":
                query_results = query_results.filter(redemptionActivity__isnull = True)
        else:
            for idNum in request.POST.keys(): 
                try:
                    voucher = Voucher.objects.get(code=idNum)
                    voucher.delete()
                except:
                    idNum = idNum
            query_results = Voucher.objects.all()
    query_results = query_results.order_by('-id')[:30]
    context = {'query_results': query_results }
    context['isRedemed'] = "All"
    try:
        for item in request.POST.keys():
            context[item] = request.POST[item]
    except:
        context = context
    return render(request,'volunteers/codeGenerator.html',context)

#Generates an 8-digit-long random code that alternates between capital letters and numbers 1-9
def generateCode():
    
    #Returns a string of a single random capitalized letter of the alphabet 
    def getRandomLetterInt():
        return 65+randint(0,25)
    
    code = ""
    letterCount = 0
    intCount = 0
    for i in range(0,6):
        if (i%2 == 0):
            letterInt = getRandomLetterInt() 
            letterCount += letterInt
            code += str(chr(letterInt))
        else:
            integer = randint(1,9)
            intCount += integer
            code += str(integer)

    endLetter = str(chr(65+(letterCount%26)))
    endInt = str(intCount%9)

    code = code + endLetter + endInt

    return code

#Checks a given code to see if it follows our voucher code rules. If it's valid, codeCheck() returns True. If not, returns False.
def codeCheck(code):
    letterCount = 0
    intCount = 0
    for i in range(0,6):
        char = code[i]
        if (i%2==0):
            letterInt = ord(char)
            if (letterInt < 65) or (letterInt > 90): #numbers chorespond to ascii characters
                print "not in range"
                return False
            letterCount += letterInt
        else:
            try:
                intCount += int(char)
            except ValueError:
                print "whoops, that isn't an INTEGER!!!"
                return False

    try:
        #check if the endLetter and endInteger match as expected. If not, return False. 
        if ( ord(code[len(code)-2]) != (65 + (letterCount%26)) or int(code[len(code)-1]) != (intCount%9) ):
            print "end character is not as expected"
            return False
    except ValueError:
        print "whoops, that isn't an INTEGER!!!!"
        return False

    return True

@user_passes_test(lambda user: user.is_staff)
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
        try:
            for i in range(int(quantity)):
                newCode = generateCode()
                while (Voucher.objects.filter(code=newCode).exists()):
                    newCode = generateCode()

                voucher = Voucher(code=newCode, credits=int(points))
                voucher.save()
                generatedVouchers.append(voucher)
        except: 
            return render(request, 'volunteers/codeGenerator.html', {})
    context = {'generatedVouchers': generatedVouchers}
    return render(request,'volunteers/viewGeneratedCodes.html',context)

@user_passes_test(lambda user: user.is_staff)
def viewGeneratedCodes(request):
    generatedVouchers = request.generatedVouchers
    context = {'generatedVouchers': generatedVouchers}
    return render(request,'volunteers/viewGeneratedCodes.html',context)

def exportCodes(request):
    generatedVouchers = Voucher.objects.all()
    now = datetime.now().strftime('%d-%b-%Y-%H-%M-%S')

    if len(generatedVouchers) == 0:
        print "THERE ARE NO VOUCHERS TO EXPORT?!?"

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="voucherCodes-'+now+'.csv"'

    writer = csv.writer(response)
    writer.writerow(['Codes', 'Credits'])

    for voucher in generatedVouchers:
        writer.writerow([str(voucher.code), str(voucher.credits)])

    return response

# decorators
def redirect_to_https(viewFunction):
    def _redirect_to_https(request, *args, **kwargs):
        if not request.is_secure():
            if not getattr(settings, "HTTPS_REDIRECT", True):
                redirect = request.build_absolute_uri(request.get_full_path()).replace("http://", "https://")
                return HttpResponseRedirect(redirect)
        return viewFunction(request, *args, **kwargs)
    return _redirect_to_https