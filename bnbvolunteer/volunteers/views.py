from django.shortcuts import render

def volunteerHome(request):
    return render(request,'volunteerHome.html')

def volunteerSubmit(request):
    date = request.POST['date']
    task = request.POST['task']
    hours = request.POST['hours']
    rate = request.POST['rate']
    earned = request.POST['earned']
    log = Userlog(user=request.user,date=date,task=task,hours=hours,rate=rate,earned=earned)
    log.save()
    return render(RequestContext(request),'volunteerHome.html')


