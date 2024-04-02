from django.contrib import admin
from .models import LeaveRequest,TeamMember,User,CheckInOut


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
    list_display = ('username', 'email', 'Address', 'Pan_Number', 'Aadhar_Number', 'phone_number','from_time', 'to_time')
    search_fields = ['username', 'email', 'phone_number'] # Define the fields to display in the admin list view

admin.site.register(User, UserAdmin)  # Register the User model with the custom admin class

@admin.register(CheckInOut)
class CheckInOutAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'phone_number', 'check_in_time', 'check_out_time', 'image_tag')
    list_filter = ('check_in_time', 'check_out_time')
    search_fields = ('user__username', 'phone_number')
    readonly_fields = ('image_tag',)

    def get_username(self, obj):
        return obj.user.username if obj.user else ''

    get_username.short_description = 'User'

    def image_tag(self, obj):
        if obj.image:
            return '<img src="{}" style="max-width:100px; max-height:100px;" />'.format(obj.image.url)
        else:
            return 'No Image'

    image_tag.allow_tags = True
    image_tag.short_description = 'Image'

    fields = ('get_username', 'phone_number', 'check_in_time', 'check_out_time', 'image', 'image_tag')

