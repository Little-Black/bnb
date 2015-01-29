from django.shortcuts import render
from django.http.response import HttpResponseRedirect, HttpResponse
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe

from bnbvolunteer import settings
from volunteers.decorators import redirect_to_https, staff_only
from volunteers.models import ActivityType, Activity, Voucher, VerificationRequest, UserProfile
from volunteers.userManagement import LoginForm, RegistrationForm, EditProfileForm, PasswordChangeForm, RequestPasswordResetForm, getIP, userDeleteAccount

from math import ceil
from random import randint
from sys import maxint
from datetime import date
from datetime import datetime, timedelta

import csv

def siteInfoContextProcessor(request):
    return {"org_name": settings.ORG_NAME, "org_name_short": settings.ORG_NAME_SHORT, "subheader": settings.SUBHEADER}

@login_required
def volunteerHome(request):
    if request.method == "POST":
        return volunteerSubmit(request)
    else:
        returnpage = 'volunteers/volunteerStaffHome.html' if request.user.is_staff else 'volunteers/volunteerHome.html'
        context = getVolunteerPageContext(request)
        return render(request, returnpage, context)

@login_required
def volunteerSubmit(request):
    returnpage = 'volunteers/volunteerHome.html'
    if request.user.has_perm('staff_status'):
        returnpage = 'volunteers/volunteerStaffHome.html'
    print "GOT SUBMISSION!!"
    try:
        user = request.user #authenticate(username='admin', password='adMIN')
    except:
        print "ERROR UGHHH"
    dateDone = request.POST['date']
    print dateDone
    if date.today() < datetime.strptime(dateDone, "%Y-%m-%d").date():
        context = getVolunteerPageContext(request)
        context['message']='Date late than today!'
        return render(request,returnpage,context)
    print request.POST['activityType']
    try:
        activityType = ActivityType.objects.filter(name=request.POST['activityType'])[0]
    except:
        activityType = None
    # activityType.save()
    if 'description' in request.POST.keys():
        description = request.POST['description']
    else:
        description = ""
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
        if len(voucher_set)==1 and not voucher_set[0] in vouchers_used:
            # print voucher
            voucher = voucher_set[0]
            totalearned+=voucher.credits
            vouchers_used.append(voucher)
            print "VALID!"
        elif len(voucher_set)==0 or voucher_set[0] in vouchers_used:
            invalid.append((voucher_code.encode('utf8')))
            invalid_boolean = "True"
        else: 
            return HttpResponse("Error: Multiple vouchers exist for that code")
    storedate = dateDone #reformat the date :/
    activity = Activity(user=user,dateDone=storedate,activityType = activityType, description=description,credits=totalearned) #request.user
    # try: 
    if len(invalid) == 0:
        activity.save()
    # except:
    #     print "ERROR"
    for voucher in vouchers_used:
        voucher.redemptionActivity = activity
        voucher.save()
    context = getVolunteerPageContext(request)
    # return HttpResponse("Hi there!")
    context['invalid_vouchers']=mark_safe(invalid)
    context['invalid_boolean']=invalid_boolean
    print invalid_boolean
    return render(request, returnpage, context)
    # return HttpResponseRedirect('/volunteer/home/','volunteers/volunteerHome.html',context)

def getVolunteerPageContext(request):
    user = request.user
    query_results = user.activity_set.all()
    total_credits = user.profile.totalCredit()
    type_choices = ActivityType.objects.values_list('name', flat=True)
    # jq = ActivityType.objects.exclude(id__in=activities)
    # type_choices = jq.values_list('name', flat=True)
    if len(type_choices) == 0:
        type_choices = ["Edit me out later","Views.py somewhere"]
    context = {'query_results': query_results,'total_credits':total_credits,'type_choices':type_choices, 'invalid_boolean':False}
    context['today'] = date.today().strftime('%Y-%m-%d')
    return context

@staff_only
def volunteerStaffHome(request):
    return volunteerHome(request)
    #Logs = Activity.objects.all()
    #try:
    #    user = request.user #authenticate(username='admin', password='adMIN')
    #except:
    #    print "Not logged in"
    #context = {'Logs': Logs}
    #return render(request,'volunteers/volunteerStaffHome.html',context)

    # try:
    #     user = request.user #authenticate(username='admin', password='adMIN')
    #     context = getVolunteerPageContext(request,user)
    # except:
    #     print "Not logged in"
    #     context = {'query_results': [],'total_credits':0,'type_choices':[]}
    # return render(request,'volunteers/volunteerHome.html',context)

@staff_only
def volunteerStaffLog(request):
    type_choices = ActivityType.objects.all()
    Logs = Activity.objects.all().order_by('-dateEntered')
    if request.method == "POST" and not 'activityType' in request.POST.keys():
        for idNum in request.POST.keys(): 
            try:
                Activity.objects.get(id=int(idNum)).delete()
            except:
                idNum = idNum
        Logs = Activity.objects.all().order_by('-dateEntered')
    if request.method == "POST" and 'activityType' in request.POST.keys():
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
        context = { 'dateDoneUp': request.POST['dateDoneUp'], 'dateDoneDown': request.POST['dateDoneDown'], 'type_choices': type_choices, 'typeSelected': request.POST['activityType'], 'creditsDown': request.POST['creditsDown'], 'creditsUp': request.POST['creditsUp']}
    else:
        context = { 'dateDoneUp': "", 'dateDoneDown': "", 'type_choices': type_choices, 'typeSelected': "All", 'creditsDown': "", 'creditsUp': ""}
    num = len(Logs)
    try:
        Logs = Logs[30*int(request.GET['page']):]
        pageNum = int(request.GET['page'])+1
    except:
        pageNum = 1
    try:
        if request.GET['page'] == "?":
            toPage = min((num-1)/30 , max(int(request.POST['toPage'])-1, 0))
            Logs = Logs[30*toPage:]
            pageNum = toPage + 1
    except:
        pageNum = 1
    Logs = Logs[:30]
    context['Logs'] = Logs
    context['num'] = num
    context['lastPage'] = max(pageNum-2, 0)
    context['nextPage'] = min(pageNum, (num-1)/30)
    context['pageNum'] = pageNum
    context['allPage'] = max((num-1)/30 + 1, 1)
    return render(request, 'volunteers/volunteerStaffLog.html', context)

@staff_only
def volunteerStaffActivity(request):
    if request.method == "POST":
        if not request.POST['activityName'] == "":
            if len(ActivityType.objects.filter(name=request.POST['activityName'])) == 0:
                ActivityType(name=request.POST['activityName']).save()
    if 'delete' in request.GET:
        ActivityType.objects.get(id=request.GET['delete']).delete()
        return HttpResponseRedirect(reverse("volunteerStaffActivity"))
    query_results = ActivityType.objects.all()
    context = {'query_results': query_results}
    return render(request, 'volunteers/volunteerStaffActivity.html', context)

@staff_only
def volunteerStaffUserSearchResult(request):
    USERS_PER_PAGE = 30
    context = dict()
    if request.method == "POST":
        lastname = request.POST['lastname'] if 'lastname'in request.POST else ""
        phone = request.POST['phone'] if 'phone' in request.POST else ""
        email = request.POST['email'] if 'email' in request.POST else ""
        try:
            creditLowerBound = int(request.POST['creditsDown'])
        except:
            creditLowerBound = 0
        try:
            creditUpperBound = int(request.POST['creditsUp'])
        except:
            creditUpperBound = maxint
        search_results_raw = User.objects.filter(last_name__icontains=lastname, profile__phone__contains=phone, email__contains=email)
        search_results_raw = filter(lambda user: creditLowerBound <= user.profile.totalCredit() <= creditUpperBound, search_results_raw)
        context.update({'lastname': lastname,
                        'phone': phone,
                        'email': email,
                        'creditsDown': request.POST.get('creditsDown'),
                        'creditsUp': request.POST.get('creditsUp')
                        })
    else:
        search_results_raw = User.objects.all()
    userCount = len(search_results_raw)
    pageCount = int(ceil(float(userCount)/USERS_PER_PAGE))
    try:
        page = min(max(1,int(request.GET['page'])),pageCount)
    except:
        page = 1
    if page != pageCount:
        search_results = map(lambda user: (user, user.profile.totalCredit()), search_results_raw[USERS_PER_PAGE*(page-1):USERS_PER_PAGE*page])
    else:
        search_results = map(lambda user: (user, user.profile.totalCredit()), search_results_raw[USERS_PER_PAGE*(page-1):])
    context['prevPage'] = max(1,page-1)
    context['nextPage'] = min(page+1, pageCount)
    context['search_results'] = search_results
    context['userCount'] = userCount
    context['pageCount'] = pageCount
    context['page'] = page
    return render(request, 'volunteers/volunteerStaffSearchResults.html', context)

@staff_only
def volunteerStaffUser(request):
    inform = ""
    type_choices = ActivityType.objects.all()
    try:
        user = User.objects.get(username=request.GET['getuser'])
    except User.DoesNotExist:
        return render(request, 'volunteers/volunteerStaffUser.html', {'inform': "User does not exist."})
    if request.method == "POST":
        if 'activityType' in request.POST:
            activityType = ActivityType.objects.get(name = request.POST['activityType'])
            try:
                addLog = Activity(user=user,  description=request.POST['description'], credits=request.POST['credits'], staff=request.user, dateDone = request.POST['dateDone'], activityType = activityType)
                if user.profile.totalCredit() + int(addLog.credits) < 0:
                    inform = "Do not have enough credits."
                else:
                    addLog.save()
            except:
                inform = "Invalid credits or Date Done."
        else:
            for idNum in request.POST: 
                try:
                    activity = Activity.objects.get(id=int(idNum))
                    activity.delete()
                except:
                    pass
    context = {'search_results':user.activity_set.all(), 'getuser':user, 'inform':inform, 'type_choices':type_choices}
    return render(request, 'volunteers/volunteerStaffUser.html', context)

@redirect_to_https
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

@redirect_to_https
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

@redirect_to_https
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
        infoForm = EditProfileForm(EditProfileForm.createUserContext(request.user))
        pwForm = PasswordChangeForm()
    returnPage = "volunteerHome"
    isStaff = False
    if request.user.is_staff:
    # if request.user.has_perm("staff_status"):
        returnPage = "volunteerStaffHome"
        isStaff = True
    return render(request, "volunteers/profile.html", {"infoForm": infoForm, "pwForm": pwForm, "returnPage": returnPage, "isStaff": isStaff})

def verify(request, code):
    cacheKey = (getIP(request), "verify")
    if cache.get(cacheKey, 0) >= 5:
        message = "You are temporarily blocked from this page because you have entered too many invalid codes."
    else:
        try:
            verificationRequests = VerificationRequest.objects.get(code=code)
            message = verificationRequests.verify()
        except VerificationRequest.DoesNotExist:
            cache.set(cacheKey, cache.get(cacheKey, 0)+1, 300)
            message = "Invalid code."
    return render(request, "volunteers/verify.html", {"message": message, "redirect_time": 3})

@login_required
def deleteAccount(request):
    userDeleteAccount(request)
    return HttpResponseRedirect(reverse("editProfile"))

@staff_only
def codeGenerator(request):
    query_results = Voucher.objects.all()
    if request.method == 'POST':
        if "isRedemed" in request.POST.keys():
            ## If the user wanted to filter vouchers
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
            vouchersToExport = []
            for idNum in request.POST.keys(): 
                ## If the user selected an export button, get the vouchers the user wants to export
                ## If not, the user meant to delete those vouchers
                    try:
                        voucher = Voucher.objects.get(code=idNum)
                        if request.GET['export'] == "Yes":
                            vouchersToExport.append(voucher)
                        else:
                            voucher.delete()
                    except:
                        idNum = idNum

            #Now that you've built the list of vouchers to export, send the lsit to exportCodes()
            if request.GET['export'] == "Yes":
                responseToExport = exportCodes(request, vouchersToExport)
                return responseToExport

            query_results = Voucher.objects.all()        
    query_results = query_results.order_by('-id')
    num = len(query_results)
    try:
        query_results = query_results[30*int(request.GET['page']):]
        pageNum = int(request.GET['page'])+1
    except:
        pageNum = 1
    try:
        if request.GET['page'] == "?":
            toPage = min((num-1)/30 , max(int(request.POST['toPage'])-1, 0))
            query_results = query_results[30*toPage:]
            pageNum = toPage + 1
    except:
        pageNum = 1
    query_results=query_results[:30]
    context = {'query_results': query_results }
    context['isRedemed'] = "All"
    for item in request.POST.keys():
        try:
            context[item] = request.POST[item]
        except:
            context = context
    context['num'] = num
    context['lastPage'] = max(pageNum-2, 0)
    context['nextPage'] = min(pageNum, (num-1)/30)
    context['pageNum'] = pageNum
    context['allPage'] = max((num-1)/30 + 1, 1)
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

@staff_only
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
            #TODO: redirect them to the same page with an error message telling the user to try again. Field checking. TODO
        try:
            for i in range(int(quantity)):
                newCode = generateCode()
                while (Voucher.objects.filter(code=newCode).exists()):
                    newCode = generateCode()
                voucher = Voucher(creator=request.user, code=newCode, credits=int(points))
                voucher.save()
                generatedVouchers.append(voucher)
        except: 
            print "Vouchers are not properly saving for some reason."
            return render(request, 'volunteers/codeGenerator.html', {})
    context = {'generatedVouchers': generatedVouchers}
    return render(request,'volunteers/viewGeneratedCodes.html',context)

@staff_only
def viewGeneratedCodes(request):
    generatedVouchers = request.generatedVouchers
    context = {'generatedVouchers': generatedVouchers}
    return render(request,'volunteers/viewGeneratedCodes.html',context)

#Exports the vouchers the current user has created in the last X minutes, which can be adjusted by changing 'minutes = X' below.
@staff_only
def exportCodes(request, specifiedVouchers = []):
    user = request.user
    minutes = 60
    days = (minutes/60.0)/24.0
    start_datetime = datetime.now()-timedelta(days=days)
    end_datetime = datetime.now()

    #If vouchers aren't specified in the arguments, look up this user's created vouchers in the past X mins and export those.
    if specifiedVouchers == []:
        generatedVouchers = Voucher.objects.filter(generateDate__range=(start_datetime, end_datetime), creator=request.user)
    else:
        generatedVouchers = specifiedVouchers

    now = datetime.now().strftime('%d-%b-%Y-%H-%M-%S')

    if len(generatedVouchers) == 0:
        print "THERE ARE NO VOUCHERS TO EXPORT"

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="voucherCodes-'+now+'.csv"'

    writer = csv.writer(response)
    writer.writerow(['Codes', 'Credits'])

    for voucher in generatedVouchers:
        writer.writerow([str(voucher.code), str(voucher.credits)])

    return response
