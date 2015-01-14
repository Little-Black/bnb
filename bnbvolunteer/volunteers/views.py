from django.shortcuts import render
from volunteers.models import *
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
import random

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

# @login_required
# def submitUpdatedProfile(request):
#     try:
#         user = request.user #authenticate(username='admin', password='adMIN')
#     except:
#         print "ERROR UGHHH"
#     firstName = request.POST['firstName']
#     lastName = request.POST['lastName']
#     email = request.POST['email']
#     phone = request.POST['phone']
#     oldPassword = request.POST['oldPassword']
#     newPassword = request.POST['newPassword']
#     newPassword2 = request.POST['newPassword2'] #will add form verification so we don't have to worry about this here
#     addressLine1 = request.POST['addressLine1']
#     addressLine2 = request.POST['addressLine2']
#     city = request.POST['city']
#     state = request.POST['state']
#     zipCode = request.POST['zipCode']

#     successNote = []
#     failedNote = []

#     #Check if the user actually made changes to any of the fields...
#     if !(user.first_name == firstName):    
#         user.first_name = firstName
#         successNote.append("First name was successfully updated!")
#     if !(user.last_name == lastName):
#         user.last_name = lastName
#         successNote.append("Last name was successfully updated!")
#     if !(user.email == email):
#         user.email = email
#         successNote.append("Email was successfully updated!")

#     oldPassIsCorrect = check_password(oldPassword, user.password)
#     if oldPassIsCorrect:
#         user.password = newPassword
#     else:
#         #Old password is wrong! Noooooo, now they must try again.
#         failedNote.append("Old password is not correct. Please try again.")

#     user.profile.phone = phone
#     user.profile.address = addressLine1+addressLine2+city+state+zipCode

#     try:
#         user.save()
#         user.profile.save()
#     except:
#         print "ERROR SAVING USER UPDATES"

#     context = {'successNote': successNote,'failedNote':failedNote}
#     return render(request,'volunteers/updateProfile.html',context)

@login_required
def codeGenerator(request):
    context = {}
    return render(request,'volunteers/codeGenerator.html',context)

#Returns a random integer between min (inclusive) to max (inclusive)
def getRandomInt(min, max):
    return random.randint(min, max)

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