import base64
from django.http import JsonResponse
from django.shortcuts import redirect, render
from .models import TeamMember
from django.contrib.auth.decorators import login_required
from .models import LeaveRequest,CheckInOut,User,Hero, Feature, Service
from .forms import SignUpForm
from datetime import datetime
from django.core.files.base import ContentFile


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
def Approvals(request):
    if request.method == 'POST':
        leave_type = request.POST.get('category')
        description = request.POST.get('description')
        
        if leave_type == 'permission':
            # For permission leave type, also get start time, end time, and description
            start_date = request.POST.get('start-date')
            start_time = request.POST.get('start-time')
            end_time = request.POST.get('end-time')
            description = request.POST.get('description')
            
            # Save the leave request to the database
            LeaveRequest.objects.create(
                leave_type=leave_type,
                start_date=start_date,
                start_time=start_time,
                end_time=end_time,
                description=description,
            )
        elif leave_type in ['half-day', 'late', 'force']:
            # For half-day, late, and force leave types, get start date and description
            start_date = request.POST.get('start-date')
            description = request.POST.get('description')
            
            # Save the leave request to the database
            LeaveRequest.objects.create(
                leave_type=leave_type,
                start_date=start_date,
                description=description,
            )
        else:
            # For other leave types, get start date, end date, and description
            start_date = request.POST.get('start-date')
            end_date = request.POST.get('end-date')
            description = request.POST.get('description')
            
            # Save the leave request to the database
            LeaveRequest.objects.create(
                leave_type=leave_type,
                start_date=start_date,
                end_date=end_date,
                description=description,
            )
        
        return JsonResponse({'success': True,'leave_type': leave_type})  # Return JSON response upon successful submission
    else:
        # Handle GET request or render the initial form page
        return render(request, 'portal/approvals.html')

@login_required
def attendance(request):
    username = request.user.username
    selected_date = request.POST.get('selected-date')
    leave_type = request.POST.get('category')

    leave_requests = LeaveRequest.objects.filter(start_date=selected_date, leave_type=leave_type)
    context = {
        'username': username,
        'leave_requests': leave_requests,
        'selected_date': selected_date  # Pass selected date to template
    }
    return render(request, 'portal/attendance.html', context)

def get_leave_requests(request):
    # Parse selected date from request
    selected_date = request.POST.get('selected-date')

    # Query leave requests for the selected date
    leave_requests = LeaveRequest.objects.filter(start_date=selected_date).values('leave_type')

    # Return leave requests as JSON response
    return JsonResponse(list(leave_requests), safe=False)

def get_checkin_data(request):
    # Parse year and month from request
    year = int(request.GET.get('year'))
    month = int(request.GET.get('month'))

    # Query check-in data for the specified year and month
    checkin_data = CheckInOut.objects.filter(
        check_in_time__year=year,
        check_in_time__month=month
    ).values('check_in_time__day')

    # Return check-in data as JSON response
    return JsonResponse(list(checkin_data), safe=False)



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



