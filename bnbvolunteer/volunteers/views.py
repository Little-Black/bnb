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
from volunteers.userManagement import LoginForm, RegistrationForm, EditProfileForm, PasswordChangeForm, RequestPasswordResetForm, userDeleteAccount

from random import randint
from datetime import date
from datetime import datetime

import csv

@login_required
def volunteerHome(request):
    print "Homepage no submit"
    try:
        user = request.user #authenticate(username='admin', password='adMIN')
        context = getVolunteerPageContext(request,user)
    except:
        print "Not logged in"
        context = {'query_results': [],'total_credits':0,'type_choices':[]}
    return render(request,'volunteers/volunteerHome.html',context)

@login_required
def volunteerSubmit(request):
    print "GOT SUBMISSION!!"
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
    # return HttpResponseRedirect('/volunteer/home/','volunteers/volunteerHome.html',context)

def getVolunteerPageContext(request,user):
    query_results = user.activity_set.all()
    total_credits = user.profile.totalCredit()
    type_choices = ActivityType.objects.values_list('name', flat=True)
    # jq = ActivityType.objects.exclude(id__in=activities)
    # type_choices = jq.values_list('name', flat=True)
    if len(type_choices) == 0:
        type_choices = ["Edit me out later","Views.py somewhere"]
    context = {'query_results': query_results,'total_credits':total_credits,'type_choices':type_choices, 'invalid_boolean':False}
    return context

@staff_only
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
    context = dict()
    if request.method == "POST":
        lastname = request.POST['lastname'] if 'lastname'in request.POST else ""
        phone = request.POST['phone'] if 'phone' in request.POST else ""
        email = request.POST['email'] if 'email' in request.POST else ""
        try:
            creditLowerBound = int(request.POST['creditsDown']) if 'creditsDown' in request.POST else 0
        except ValueError:
            creditLowerBound = 0
        try:
            creditUpperBound = int(request.POST['creditsUp']) if 'creditsUp' in request.POST else 999999
        except ValueError:
            creditUpperBound = 999999
        search_results_raw = User.objects.filter(last_name__icontains=lastname, profile__phone__contains=phone, email__contains=email)
        search_results_raw = filter(lambda user: creditLowerBound <= user.profile.totalCredit() <= creditUpperBound, search_results_raw)
        context.update({'lastname': lastname,
                        'phone': phone,
                        'email': email,
                        'creditsDown': creditLowerBound,
                        'creditsUp': creditUpperBound
                        })
    else:
        search_results_raw = User.objects.all()
    search_results = map(lambda user: (user, user.profile.totalCredit()), search_results_raw)
    context.update({'search_results': search_results, 'type_choices': ActivityType.objects.all()})
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
        infoForm = EditProfileForm(EditProfileForm.createUserContext(request.user))
        pwForm = PasswordChangeForm()
    returnPage = "volunteerHome"
    if request.user.has_perm("staff_status"):
        returnPage = "volunteerStaffHome"
    return render(request, "volunteers/profile.html", {"infoForm": infoForm, "pwForm": pwForm, "returnPage": returnPage})

def verify(request, code):
    cacheKey = (request.META["REMOTE_ADDR"], "verify")
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

@login_required
def search(request):
    context = {}
    return render(request,'volunteers/search.html',context)

@login_required
def updateProfile(request):
    context = {}
    return render(request,'volunteers/updateProfile.html',context)

@staff_only
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
    try:
        for item in request.POST.keys():
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

@staff_only
def viewGeneratedCodes(request):
    generatedVouchers = request.generatedVouchers
    context = {'generatedVouchers': generatedVouchers}
    return render(request,'volunteers/viewGeneratedCodes.html',context)

@staff_only
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