from django.http import JsonResponse
from django.shortcuts import redirect, render
from .models import TeamMember
from django.contrib.auth.decorators import login_required
from .models import LeaveRequest
from .forms import SignUpForm



def home(request):
    return render(request, 'portal/home.html')

def camera(request):
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
    leave_requests = LeaveRequest.objects.all().values('start_date', 'end_date', 'description','leave_type')
    leave_requests_list = list(leave_requests)
    return JsonResponse(list(leave_requests_list), safe=False)

def salary(request):
    return render(request, 'portal/salary.html')

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



