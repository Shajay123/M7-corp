from django.contrib import admin
from .models import LeaveRequest,TeamMember,User


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'designation', 'position', 'display_image']
    search_fields = ['name', 'designation', 'position']

    def display_image(self, obj):
        return obj.image.url if obj.image else None

    display_image.short_description = 'Image'


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('leave_type', 'start_date', 'end_date', 'start_time', 'end_time', 'description')
    list_filter = ('leave_type', 'start_date', 'end_date')
    search_fields = ('leave_type', 'description')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.filter(user=request.user)
        return queryset
    
    
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'Address', 'Pan_Number', 'Aadhar_Number', 'Phone_Number','from_time', 'to_time')
    search_fields = ['username', 'email', 'Phone_Number'] # Define the fields to display in the admin list view

admin.site.register(User, UserAdmin)  # Register the User model with the custom admin class