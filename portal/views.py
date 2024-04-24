import base64
from django.db.models import Count
from django.http import JsonResponse
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
from django.contrib.auth import logout as django_logout
from django.contrib.auth import authenticate, login

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
            # If user doesn't exist, redirect to sign-up page
            return redirect('signup')  # Assuming 'signup' is the URL name for sign-up page

        # Save the check-in time
        check_in_time = datetime.now()

        # Save the captured image to a directory based on the username with the current date
        username = user.username
        date_str = check_in_time.strftime('%Y-%m-%d')
        
        # Decode the base64 image data
        image_data_url = request.POST.get('image')
        format, imgstr = image_data_url.split(';base64,')
        ext = format.split('/')[-1]
        image_data = ContentFile(base64.b64decode(imgstr), name=f'{username}_{date_str}.{ext}')

        # Save to CheckInOut model
        check_in_out = CheckInOut.objects.create(user=user, phone_number=mobile, check_in_time=check_in_time, image=image_data)

        # Redirect to some success page or do further processing
        return redirect('signup_success')  # Redirect to success page

    return render(request, 'portal/camera.html')



@login_required
def attendance(request):
    username = request.user.username
    context = {
        'username': username,
    }
    return render(request, 'portal/attendance.html', context)



def get_checkin_data(request):
    checkin_data = CheckInOut.objects.all()

    events = [{
        'title': f"Check-in - {data.get_username_from_phone_number()}",
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
            return redirect('signup_success')  # Redirect to success page
    else:
        form = SignUpForm()
    return render(request, 'portal/signup.html', {'form': form})


def signup_success(request):
    return render(request, 'portal/signup_success.html')

def success(request):
    return render(request, 'portal/success.html')




def add_event(request):
    if request.method == "POST":
        form = EventsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all_events')  # Assuming you have a view named 'all_events'
    else:
        form = EventsForm()
    
    return render(request, 'portal/add_event.html', {'form': form})


def all_events(request):
    all_events = Events.objects.all()
    events_list = []

    for event in all_events:
        start = event.start.strftime("%Y-%m-%d %H:%M:%S") if event.start else None
        end = event.end.strftime("%Y-%m-%d %H:%M:%S") if event.end else None

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
        email = request.POST.get('email')

        user = authenticate(request, username=username, password=password,email=email)
        
        if user is not None:
            login(request, user)
            request.session['username'] = username  # Store the username in session
            return redirect('login_sucess')  
            
    
    return render(request, 'portal/login.html')



@login_required
def logout_view(request):
    django_logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('login')



def login_sucess(request):
    return render(request, 'portal/login_sucess.html')


