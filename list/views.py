from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Profile, Event, Contact
from django_tables2 import MultiTableMixin, RequestConfig, SingleTableMixin, SingleTableView
from .tables import CheckboxTable
from .forms import EditForm, sendForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mass_mail
from django.contrib.auth.decorators import user_passes_test




# Create your views here.
def home(request):
    # login authentication
    if request.user.is_authenticated:
        return redirect('profile')
    else:
        return redirect('loginuser')

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'list/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'list/loginuser.html',
                          {'form': AuthenticationForm(), 'error': 'Username and password are incorrect'})
        else:
            login(request, user)
            return redirect('profile')

@login_required
def userpage(request):
    eventlist = Profile.objects.get(user= request.user)
    eventlistitems = eventlist.event.all()
    if len(eventlistitems) == 1:
        Event_id = eventlistitems[0].event_id
        return redirect('../' + Event_id)
    return render(request, 'list/profile.html', {'eventlistitems':eventlistitems})

@login_required
def contact(request, Contact_id):
    item = get_object_or_404(Contact, pk=Contact_id)
    Event_id = item.event
    event =str(Event_id)

    intaial_data = {
        'contact_name': item.contact_name,
        'contact_organisation': item.contact_organisation,
        'contact_email': item.contact_email,
        'contact_mobile': item.contact_mobile,
        'startlist': item.startlist,
        'results': item.results,
        'communiques': item.communiques,

    }
    if request.method == 'GET':
        return render(request, 'list/contact.html', {'form': EditForm(intaial_data)})
    else:
        if request.user.is_authenticated:
            form = EditForm(request.POST)
            form.user = request.user
            if form.is_valid():
                name = form.cleaned_data['contact_name']
                organisation = form.cleaned_data['contact_organisation']
                email = form.cleaned_data['contact_email']
                mobile = form.cleaned_data['contact_mobile']
                startlist = form.cleaned_data['startlist']
                results = form.cleaned_data['results']
                communiques = form.cleaned_data['communiques']
                reg = Contact(id=Contact_id, contact_name=name, contact_organisation=organisation,
                           contact_email=email, contact_mobile=mobile, startlist=startlist, results=results,
                              communiques = communiques, event = Event_id)
                reg.save()
                return redirect('../../'+event)
            else:
                return render(request, 'list/contact.html',
                              {'form': EditForm(), 'error': 'That number is taken, try again with another number'})
        else:
            return render(request, 'list/contact.html', {'form': EditForm()})

@login_required
def new(request, Event_id):
    item = get_object_or_404(Event, pk=Event_id)


    if request.method == 'GET':
        return render(request, 'list/new.html', {'form': EditForm()})
    else:
        if request.user.is_authenticated:
            form = EditForm(request.POST)
            form.user = request.user
            if form.is_valid():
                name = form.cleaned_data['contact_name']
                organisation = form.cleaned_data['contact_organisation']
                email = form.cleaned_data['contact_email']
                mobile = form.cleaned_data['contact_mobile']
                startlist = form.cleaned_data['startlist']
                results = form.cleaned_data['results']
                communiques = form.cleaned_data['communiques']
                reg = Contact(contact_name=name, contact_organisation=organisation,
                           contact_email=email, contact_mobile=mobile, startlist=startlist, results=results,
                              communiques = communiques, event= item)
                reg.save()
                return redirect('../')
            else:
                return render(request, 'list/new.html',
                              {'form': EditForm(), 'error': 'please try again'})
        else:
            return render(request, 'list/new.html', {'form': EditForm()})

@login_required
def eventpage(request, Event_id):
    contactlist = Contact.objects.filter(event = Event_id)
    eventlist = Event.objects.filter(event_id= Event_id)
    table = CheckboxTable(Contact.objects.filter(event = Event_id))
    return render(request, 'list/event.html', {'contactlist':contactlist, 'table':table, 'eventlist':eventlist})

@user_passes_test(lambda u: u.is_superuser)
def sendemail(request):
    if request.method == 'GET':
        return render(request, 'list/email.html', {'form': sendForm()})
    else:
        if request.user.is_authenticated:
            form = sendForm(request.POST)
            form.user = request.user
            if form.is_valid():
                e1 = form.cleaned_data['event']
                event = Event.objects.filter(event_id=e1)
                url = form.cleaned_data['URL']
                email_option = form.cleaned_data['email_option']
                stagenumber = form.cleaned_data['stagenumber']
                comment = form.cleaned_data['comment']
                updatecomment = ''
                for i in range(len(comment)):
                    if comment[i] == "\n":
                        updatecomment += "<br>"
                    else:
                        updatecomment += comment[i]

                if email_option == "startlist":
                    queryset = Contact.objects.filter(event=e1, startlist=True)
                    option = 'Startlist'
                    message = "Please find the link to view the official startlist of the " + event[0].event_name + ' here:<br>'+"<a href="+url+">"+event[0].event_name+"-Startlist</a><br> <br> Regards,<br>Sport Services & Technology"
                    message_nonhtml = "Please find the link to view the official startlist of the " + event[0].event_name + " at - " + url
                elif email_option == "results":
                    queryset = Contact.objects.filter(event=e1, results=True)
                    option = "Results - Stage " + stagenumber
                    message = "Please find the link to view the official results of the " + event[0].event_name + ' stage ' + stagenumber + ' here:<br>'+"<a href="+url+">"+event[0].event_name+"-Results</a><br> <br>Regards,<br>Sport Services & Technology"
                    message_nonhtml = "Please find the link to view the official results of the " + event[0].event_name + ' stage ' + stagenumber + ' - ' + url
                elif email_option == "communiques":
                    queryset = Contact.objects.filter(event=e1, communiques=True)
                    option = "Communique" + " - " + event[0].event_name
                    message = "Please find below a Communique from the Commissaires Panel: <br>" + updatecomment
                    message_nonhtml = "Please find a Communique from the Commissaires Panel - " + comment

                emailaddress = []
                for i in queryset:
                    emailaddress.append(i.contact_email)
                for i in range(len(emailaddress)):
                    subject, from_email, to = event[0].event_name + '-' + option, 'results@sport-st.com', emailaddress[i]
                    text_content = message_nonhtml
                    html_content = '<p>'+message+'</p>'
                    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
                return redirect('profile')

            else:
                return render(request, 'list/email.html',
                              {'form': sendForm(), 'error': 'Please select email option'})

        else:
            return render(request, 'list/email.html', {'form': sendForm(), 'error': 'please try again'})

@login_required
def delete(request, Contact_id):
    item = get_object_or_404(Contact, pk=Contact_id)
    Event_id = item.event_id
    item.delete()
    return redirect('../../../'+Event_id)

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
