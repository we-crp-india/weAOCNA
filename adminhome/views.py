from cgi import print_environ
from unittest import removeResult
import django
from django.shortcuts import redirect, render
from django.http import HttpResponse
from client.models import Resque
from django.urls import path
from . import views
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime as d
from adminhome.models import Volunteer

#login user
def home(request):
    group = None
    admin_groups = ["admins"]
    generic_groups = ["volunteers"]
    if request.user.is_authenticated:
            group = request.user.groups.all()[0].name
            if group in admin_groups:
                return redirect('dashboard')
            elif group in generic_groups:
                return redirect('update')
    if request.method == "POST":
        user = request.POST["username"]
        passwd = request.POST["passwd"]
        user_obj = authenticate(request,username = user,password = passwd) 
        if user_obj is not None:
            login(request,user_obj)
            group = request.user.groups.all()[0].name
            if group in admin_groups:
                return redirect('dashboard')
            elif group in generic_groups:
                return redirect('update')
            else:
                return redirect('error')
        else:
            return redirect('error')
    return render(request,'adminhome/log.html')

#logout user
def logoutUser(request):
    logout(request)
    return redirect('login')
    
#dashboard
@login_required(login_url='login')
def dash(request):
    allowed_roles = ["admins"]
    if request.user.groups.all()[0].name not in allowed_roles:
        return redirect('error')
    if request.method == "POST":
        id = request.POST["searchid"]
        case = Resque.objects.all().filter(id=id)
        date1 = request.POST["search1"]
        if len(case) == 0 and date1 == "":
            messages.error(request,"No data found")
        else:
            request.session["case_id"] = id
            date2 = request.POST["search2"]
            request.session["date_1"] = date1
            request.session["date_2"] = date2
            return redirect('details')
    resque = Resque.objects.all()
    total_cases = resque.count()
    recents = Resque.objects.all()[total_cases-5:total_cases]
    recents = recents[::-1]
    open_cases = resque.filter(status='Open').count()
    pending = resque.filter(status='Pending').count()
    closed = resque.filter(status='Closed').count()
    context = {'total_cases':total_cases,
                'open_cases':open_cases,
                'pending':pending,
                'closed':closed,
                'recents':recents
    }
    return render(request,'adminhome/dashboard.html',context)

@login_required(login_url='login')
def updateCase(request):
    if request.method == "POST":
        caseid = request.POST["caseid"]
        curr_status = request.POST["newstatus"]
        try:
            case = Resque.objects.get(id=caseid)
            case.status = curr_status
            case.save()
            messages.success(request,"Data updated successfully")
            object = Volunteer.objects.get(id = case.vol)
            object.status = "Free"
            object.save()
        except:
            messages.error(request,"No Data Found")
    return render(request,'adminhome/update.html')


def ErrorFound(request):
    context = {
        'back':'login'
    }
    return render(request,'adminhome/error.html')

def Details(request):
    try:
        if request.session.has_key('case_id') and request.session["case_id"] != "":
            id = request.session["case_id"]
            case = Resque.objects.all().filter(id=id)
            # if case.count() == 0:
            #     return redirect('error')
            context = {
                'case':case,
                'id':id,
                'datefrom':"NA",
                'dateto':"NA"
            }
        elif request.session.has_key('date_1'):
            date1 = request.session["date_1"]
            date2 = request.session["date_2"]
            all_cases = Resque.objects.all()
            d1 = d.strptime(date1,'%Y-%m-%d')
            d2 = d.strptime(date2,'%Y-%m-%d')
            cases = list()
            for query in all_cases:
                check_data = d.strptime(query.date,'%Y-%m-%d')
                if check_data >= d1 and check_data <= d2:
                    cases.append(query)
            today = d.now()
            if d2 > today:
                dateto = today.strftime('%Y-%b-%d')
            else:
                dateto = d2.strftime('%Y-%b-%d')
            context = {
                'case':cases,
                'id':"NA",
                'datefrom':d1.strftime('%Y-%b-%d'),
                'dateto':dateto
            }
        else:
            return redirect('error') 
    except:
        return redirect('error')
    return render(request,'adminhome/details.html',context)