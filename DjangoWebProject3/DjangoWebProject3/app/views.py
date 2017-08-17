"""
Definition of views.
"""

from django.shortcuts import render, redirect
from django.views.generic.edit import DeleteView
from django.http import HttpRequest, HttpResponse
from django.template import RequestContext
from datetime import timedelta, date
import datetime
import calendar
import csv
import re
from app.forms import myForm, ConcediuForm, BootstrapAuthenticationForm, OOHRequestForm, ProfileForm, PontajForm
from django.core.mail import EmailMessage
from django.core.mail import BadHeaderError
import app.createConcediu
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from app.models import Concediu, OOHRequest, Profile, Pontaj
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.utils.timezone import now
from app import createConcediu
from app import pontaj

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('profile')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def profile(request):
    if request.method=='GET':
        form=ProfileForm()
    else:
        form=ProfileForm(request.POST)
        if form.is_valid():
            username = request.user.username
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            email_address=form.cleaned_data['email_address']
            marca=form.cleaned_data['marca']
            CNP=form.cleaned_data['CNP']
            location=form.cleaned_data['location']
            team=form.cleaned_data['team']
            team_leader_email=form.cleaned_data['team_leader_email']
            User.objects.filter(username=request.user.username).update(first_name=first_name, last_name=last_name)
            profile=Profile(username=username,first_name=first_name,last_name=last_name, email_address=email_address,marca=marca, CNP=CNP, location=location, team=team, team_leader_email=team_leader_email)
            profile.save()
            return redirect('home')
    return render(request, 'profile.html', {'form':form})


@login_required(login_url="/login/")
def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            
        }
    )
@login_required(login_url="/login/")
def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            
        }
    )
@login_required(login_url="/login/")
def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            
        }
    )

@login_required(login_url="/login/")
def success(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'success.html',
        {
            'title':'success',
            'message':'success',
            
        }
    )


def email(request):
    if request.method == 'GET':
        form = myForm()
    else:
        form = myForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            team_leader_email = form.cleaned_data['team_leader_email']
            days_off = form.cleaned_data['days_off']
            try:
                email=EmailMessage(subject="Pontaj pentru luna 8"  + " " +full_name, body="Please validate my file.",from_email='internalapppontaj@gmail.com',to=[team_leader_email], reply_to=['myheroalinabrinza95@gmail.com'])
                email.send()
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, "email.html", {'form': form})

################################################################################################################################
#if request==GET that means that the user requested to fill in the form
#if request==POST that means that he filled in the form and is ready to submit
#is_valid cheks if the fields are filled in correctly
#if yes, it stores in variables the value from the form
#creates an Model object from "Concediu" model, and saves it into the database using the values entered by the user in the form
#creates a pdf file to be send to the teamleader without saving it in the database
#call the function app.createConcediu.concediu which fill in the blank pdf with the information from the user
#send an email from internalapppontaj@gmail.com to the teamleader
#sets the reply_to to the email of the sender in order to send a validation reply without entering his/her email address
#EmailMessage uses TLS to assure a secure channel when sending the email
#use caes: if the submit gave an Invalid header found, the user is asked to fill in the form again
#else: he is redirected to the success.html file where he is informed that the mail was successfully sent
################################################################################################################################

@login_required(login_url="/login/")
def concediu(request):
    user_name=request.user.username
    if request.method == 'GET':
        form = ConcediuForm()
        
    else:
        form = ConcediuForm(request.POST)
        if form.is_valid():

            #full_name = form.cleaned_data['full_name']
            #email_address = form.cleaned_data['email_address']
            full_name=str(Profile.objects.only('first_name').get(username=user_name).first_name)+" "+str(Profile.objects.only('last_name').get(username=user_name).last_name)
            email_address=Profile.objects.only('email_address').get(username=user_name).email_address
            team_leader_name = form.cleaned_data['team_leader_name']
            days_off = form.cleaned_data['days_off']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            #team_leader_email_address = form.cleaned_data['team_leader_email_address']
            team_leader_email_address=Profile.objects.only('team_leader_email').get(username=user_name).team_leader_email

            User.objects.filter(username=request.user.username).update(email=email_address, first_name=full_name)

            concediu=Concediu(full_name=full_name, email_address=email_address,
                              team_leader_name=team_leader_name,days_off=days_off,
                              start_date=start_date,end_date=end_date,team_leader_email_address=team_leader_email_address)
            concediu.save()
            
            mycanvas=canvas.Canvas("concediu.pdf", pagesize=letter)            
            app.createConcediu.concediu(full_name,team_leader_name,days_off,start_date,end_date)
            try:
                email=EmailMessage(subject="Concediu"  + " " +full_name,from_email='internalapppontaj@gmail.com',to=[team_leader_email_address], reply_to=[email_address])
                email.attach_file("concediu.pdf")
                email.send()
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, "concediu.html", {'form': form})

#list view for a TL who manages the holiday requests
class ConcediuView(generic.ListView):

    template_name='concediuManagement.html'

    def get_queryset(self):
        return Concediu.objects.filter(flag=False, team_leader_email_address=self.request.user)

#detail view for a TL who manages the holiday requests
class ConcediuDetailsView(generic.DetailView):
    model=Concediu
    template_name='concediuManagementDetails.html'  

#function for validate a holiday request as a TL
def edit(request):
    username=None
    concediu_id = request.POST['concediu']
    if request.user.is_authenticated():
        username=request.user.username
        c=Concediu.objects.filter(pk=concediu_id)
    c.update(flag=True)
    #return HttpResponse(Concediu.objects.values_list('full_name', flat=True).get(pk=concediu_id))
    return redirect('success')

#View for in pending holiday requests for a normal user 
class InPendingView(generic.ListView):
    template_name='inPending.html'
    def get_queryset(self):
        return Concediu.objects.filter(flag=False,full_name=self.request.user.first_name)

#view for approved holiday requests for a normal user
class ApprovedView(generic.ListView):
    template_name='approved.html'
    def get_queryset(self):
        return Concediu.objects.filter(flag=True,full_name=self.request.user.first_name)

@login_required(login_url="/login/")
def concediuManagement(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'concediuManagement.html',
        {
            'title':'Concediu Management',
            'message':'Concediu Management page.',
            
        }
    )
############################################################################################


@login_required(login_url="/login/")
def oohrequest(request):
    if request.method=='GET':
        form=OOHRequestForm()
    else:
        form=OOHRequestForm(request.POST)
        if form.is_valid():
           full_name=request.user.first_name
           day=form.cleaned_data['day']
           worked_time=form.cleaned_data['worked_time']
           incident_number=form.cleaned_data['incident_number']
           #team_leader_email=form.cleaned_data['team_leader_email']
           team_leader_email=Profile.objects.only('team_leader_email').get(username=request.user.username).team_leader_email

           oohrequest=OOHRequest(full_name=full_name,day=day,worked_time=worked_time,incident_number=incident_number,team_leader_email=team_leader_email)
           oohrequest.save()
           return redirect('success')
    return render(request,"oohrequest.html", {'form':form})

#View for in pending ooh requests for a normal user 
class InPendingOOHView(generic.ListView):
    template_name='oohrequestInPending.html'
    def get_queryset(self):
        return OOHRequest.objects.filter(flag=False,full_name=self.request.user.first_name)

#view for approved ooh requests for a normal user
class ApprovedOOHView(generic.ListView):
    template_name='oohrequestApproved.html'
    def get_queryset(self):
        return OOHRequest.objects.filter(flag=True,full_name=self.request.user.first_name)


#List View for OOH requests as a TL
class OOHRequestView(generic.ListView):

    template_name='oohrequestManagement.html'

    def get_queryset(self):
        return OOHRequest.objects.filter(flag=False, team_leader_email=self.request.user)

#detail view for a TL who manages the OOH requests
class OOHRequestDetailsView(generic.DetailView):
    model=OOHRequest
    template_name='oohrequestManagementDetails.html'

#function for validate an oohrequest as a TL
def validate(request):
    username=None
    oohrequest_id = request.POST['oohrequest']
    if request.user.is_authenticated():
        username=request.user.username
        c=OOHRequest.objects.filter(pk=oohrequest_id)
    c.update(flag=True)
    #return HttpResponse(OOHRequest.objects.values_list('full_name', flat=True).get(pk=oohrequest_id))   
    return redirect('success')



######################################################################################
@login_required(login_url="/login/")
def generatePontaj(request):
    #assert isinstance(request, HttpRequest)
    if request.method=='POST':
        return redirect(request,'pont')
    return render(
        request,
        'generatePontaj.html',
        {
            'title':'Generate pontaj',
            'message':'Generate Pontaj page.',            
        }
    )

def pont(request):
        value=request.POST.get('pontaj')
        if request.user.is_authenticated():
            user_name=request.user.username
            firstname=Profile.objects.only('first_name').get(username=user_name).first_name
            lastname =Profile.objects.only('last_name').get(username=user_name).last_name
            email    =Profile.objects.only('email_address').get(username=user_name).email_address
            marca    =Profile.objects.only('marca').get(username=user_name).marca
            cnp      =Profile.objects.only('CNP').get(username=user_name).CNP
            locatia  =Profile.objects.only('location').get(username=user_name).location
            echipa   =Profile.objects.only('team').get(username=user_name).team
            TLemail  =Profile.objects.only('team_leader_email').get(username=user_name).team_leader_email
            concediu, oohrequest=False, False


            today=date.today()
            range_from=str(today.year)+"-"+str(today.month)+"-01"
            range_to=str(today.year)+"-"+str(today.month)+"-"+str(calendar.monthrange(today.year,today.month)[1])

            date_beginning,date_ending="",""
            days_off=0
            #user_concediu=Concediu.objects.filter(start_date__range=["2017-08-01","2017-08-31"], full_name=request.user.first_name)
            #if Concediu.objects.filter(start_date__range=[range_from,range_to], full_name=request.user.first_name)!=[]:
            try:
                for userconcediu in Concediu.objects.filter(start_date__range=[range_from,range_to], full_name=request.user.first_name, flag=True):
                    startdate=userconcediu.start_date
                    enddate=userconcediu.end_date
                    concediu=True

                    date_beginning=date_beginning+" "+str(userconcediu.start_date)
                    date_ending=date_ending+" "+str(userconcediu.end_date)


                    start_date=str(startdate)
                    end_date=str(enddate)

                    start_date1=start_date.split('-')
                    end_date1=end_date.split('-')

                    start_year, start_month, start_day = int(start_date1[0]), int(start_date1[1]), int(start_date1[2])
                    end_year, end_month, end_day = int(end_date1[0]), int(end_date1[1]), int(end_date1[2])

                    fromdate=datetime.date(start_year, start_month, start_day-1)
                    todate = datetime.date(end_year, end_month, end_day)
                    if(start_month==end_month):
                       fromdate = fromdate
                       todate = todate
                    elif ((start_month<end_month and start_year==end_year) or (start_month>end_month and start_year<end_year)):
                       fromdate=date(start_year,start_month,start_day-1)
                       last=calendar.monthrange(start_year,start_month)
                       last=last[1]
                       todate=date(start_year,start_month,last)

                    daygenerator = (fromdate + timedelta(x + 1) for x in xrange((todate - fromdate).days))
                    week_days = sum(1 for day in daygenerator if day.weekday() < 5)+1
                    days_off=days_off+week_days
            except:
                pass
            
            oohdate,incident="",""
            hours=0
            #user_oohrequest=OOHRequest.objects.filter(day__range=["2017-08-01","2017-08-31"], full_name=request.user.first_name)
            try:
            #if OOHRequest.objects.filter(day__range=[range_from,range_to], full_name=request.user.first_name)!=[]:
                for useroohrequest in OOHRequest.objects.filter(day__range=[range_from,range_to], full_name=request.user.first_name, flag=True):
                    oohdate=oohdate + " " + str(useroohrequest.day)
                    incicent=incident + " " + str(useroohrequest.incident_number)
                    hours=hours + int(useroohrequest.worked_time)
                    oohrequest=True
            except:
                pass


            with open('pontaj.csv','w') as csvfile:
                fieldnames=['Prenume','Nume','Marca','CNP','Locatia','Echipa','Email TL']
                writer=csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow({'Prenume' : firstname,'Nume': lastname,'Marca':marca,'CNP':cnp,'Locatia':locatia,'Echipa':echipa,'Email TL':TLemail})

                fieldnames1 = ['Concediu']
                writer1=csv.DictWriter(csvfile,fieldnames=fieldnames1)
                if concediu==True:
                    
                    fieldnames1.insert(len(fieldnames1)+1,'Start')
                    fieldnames1.append('End')
                    fieldnames1.insert(len(fieldnames1)+1,'Zile libere')
                    writer1.writeheader()                    

                    writer1.writerow({'Concediu':concediu,'Start':date_beginning,'End':date_ending,'Zile libere':days_off})
                else:
                    writer1.writeheader()
                    writer1.writerow({'Concediu': concediu})

                fieldnames2 = ['OOH']
                writer2=csv.DictWriter(csvfile, fieldnames=fieldnames2)
                if oohrequest==True:
                    fieldnames2.insert(len(fieldnames2)+1,'Day called')
                    fieldnames2.append('Incident number')
                    fieldnames2.append('Hours spent')
                    writer2.writeheader()
                    writer2.writerow({'OOH':oohrequest,'Day called':oohdate,'Incident number':incicent,'Hours spent':hours})
                else:
                    writer2.writeheader()
                    writer2.writerow({'OOH':oohrequest})
            try:
                email=EmailMessage(subject="Pontaj"  + " " +firstname,from_email='internalapppontaj@gmail.com',to=['myheroalinabrinza95@gmail.com', email], reply_to=[email])
                email.attach_file("pontaj.csv")
                email.send()
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            #return HttpResponse(str(firstname)+" "+str(lastname)+" " +", your pontaj was successfully generated and sent to your team leader!")
            return redirect('success')
