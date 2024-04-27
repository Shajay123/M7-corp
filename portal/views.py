import base64
from django.db.models import Count
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect, render
from .models import TeamMember
from django.contrib.auth.decorators import login_required
from .models import CheckInOut,User,Hero,Feature,Service
from .forms import EventsForm, SignUpForm
from datetime import datetime
from django.core.files.base import ContentFile
from django.http import JsonResponse 
from.models import Events
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings


def home(request):
    hero = Hero.objects.first()  # Assuming you only have one Hero instance
    features = Feature.objects.all()
    services = Service.objects.all()
    context = {
        'hero': hero,
        'features': features,
        'services': services,
    }
    return render(request, 'portal/home.html', context)

@login_required
def camera(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        
        try:
            user = User.objects.get(phone_number=mobile)
        except User.DoesNotExist:
            return redirect('signup')
        
        check_in_time = datetime.now()
        current_time = datetime.now().strftime('%H%M%S')
        
        date_str = check_in_time.strftime('%Y-%m-%d')
        
        image_data_url = request.POST.get('image')
        
        try:
            format, imgstr = image_data_url.split(';base64,')
            ext = format.split('/')[-1]
            image_data = ContentFile(base64.b64decode(imgstr), name=f'{user.username}_{date_str}_{current_time}.{ext}')
        except Exception as e:
            print(f"Error decoding image: {e}")
            return HttpResponseBadRequest("Invalid image data")

        CheckInOut.objects.create(user=user, phone_number=mobile, check_in_time=check_in_time, image=image_data)
        
        return redirect('signup_success')

    return render(request, 'portal/camera.html')


@login_required
def attendance(request):
    username = request.user.username
    context = {'username': username}
    return render(request, 'portal/attendance.html', context)



def get_checkin_data(request):
    checkin_data = CheckInOut.objects.all()

    events = [{
        'title': f"Check-in",
        'start': data.check_in_time.strftime('%Y-%m-%dT%H:%M:%S'),
        'end': data.check_out_time.strftime('%Y-%m-%dT%H:%M:%S') if data.check_out_time else None,
        'allDay': False
    } for data in checkin_data]

    return JsonResponse(events, safe=False)



@login_required
def team(request):
    team_members = TeamMember.objects.all()
    return render(request, 'portal/team.html', {'team_members': team_members})


def signup(request):
    if request.method == 'POST':
        
        form = SignUpForm(request.POST)  
        if form.is_valid():  
            form.save() 
            return redirect('signup_success')  
    else:
        
        form = SignUpForm()  
    
    return render(request, 'portal/signup.html', {'form': form})


def signup_success(request):
    return render(request, 'portal/signup_success.html')




def add_event(request):
    if request.method == "POST":
        form = EventsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('attendance')  # Assuming you have a view named 'all_events'
    else:
        form = EventsForm()
    
    return render(request, 'portal/add_event.html', {'form': form})



def all_events(request):
    all_events = Events.objects.all()
    events_list = []

    for event in all_events:
        start = event.start.strftime("%Y-%m-%d") if event.start else None
        end = event.end.strftime("%Y-%m-%d") if event.end else None

        if not start or not end:
            continue

        events_list.append({
            'title': event.name,
            'id': event.id,
            'start': start,
            'end': end,
        })

    return JsonResponse(events_list, safe=False)

def update(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    id = request.GET.get("id", None)
    event = Events.objects.get(id=id)
    event.start = start
    event.end = end
    event.name = title
    event.save()
    data = {}
    return JsonResponse(data)
 
def remove(request):
    id = request.GET.get("id", None)
    event = Events.objects.get(id=id)
    event.delete()
    data = {}
    return JsonResponse(data)




def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            request.session['username'] = username  # Store the username in session
            return redirect('home')  # Redirect to the dashboard or home page
            
    return render(request, 'portal/login.html')



@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('login')



def login_sucess(request):
    return render(request, 'portal/login_sucess.html')




def sendEmail(request):
    if request.method == 'POST':
        # You might want to validate the form data using Django forms here.

        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')

        template = render_to_string('portal/email_template.html', {'name': name, 'email': email, 'message': message})

        subject = request.POST.get('subject', 'Default Subject')  # Provide a default subject if not present

        email = EmailMessage(
            subject,
            template,
            settings.EMAIL_HOST_USER,
            ['shajaygopi2001@gmail.com']
        )

        email.fail_silently = False
        email.send()

        return render(request,'portal/email_sent.html')