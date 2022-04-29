from pyexpat import model
from django.shortcuts import render
from django.http import HttpResponse
from client.models import Resque
from datetime import datetime
from django.contrib import messages
from django.core.mail import send_mail
from adminhome.models import Volunteer

def home(request):
    return render(request,'client/home.html')

def team(request):
    return render(request,'client/team.html')

def locateus(request):
    return render(request,'client/locateus.html')

def about(request):
    return render(request,'client/about.html')

def adopt(request):
    return render(request,'client/adopt.html')

def register(request):
    if request.method == "POST":
        fn = request.POST["fname"]
        ln = request.POST["lname"]
        em = request.POST["email"]
        ph = request.POST["phn_no"]
        addr = request.POST["text1"]
        bd = request.POST["brdn"]
        try:
            vc = request.POST["darkmode"]
        except:
            vc = "no"
        re = request.POST["text2"]
        cn = request.POST["sellist1"]
        now = str(datetime.now())
        dt = datetime.now().strftime('%Y-%m-%d')
        uid = now[2:4]+now[5:7]+now[8:10]+now[11:13]+now[14:16]+now[17:19]+now[20:]
        vid = placevolunteer()
        data = Resque(id=uid,firstname=fn.capitalize(),lastname=ln.capitalize(),email=em,phone=ph,addrs=addr,breed=bd,vaccination=vc,reason=re,condition=cn,date=dt,status="Open",vol=vid)
        data.save()
        if cn == "Severe" or cn == "Not Good":
            messages.success(request,"Data submitted successfully.A volunteer will contact you soon.")
        else:
            messages.success(request,"Data submitted successfully.A volunteer will contact you within tomorrow.")
    return render(request,'client/register.html')

#Sending registration ticket to the user.

#Finding the free volunteer.
def placevolunteer():
    object  = Volunteer.objects.all()
    search = object.filter(status='Free')
    if len(search) == 0:
        return "Pending..."
    else:
        data = Volunteer.objects.get(id = search[0].id)
        data.status = "Deployed"
        data.save()
        return search[0].id
