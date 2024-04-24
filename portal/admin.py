from django.contrib import admin
from .models import TeamMember,User,CheckInOut,Hero, Feature, Service


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'designation', 'position', 'display_image']
    search_fields = ['name', 'designation', 'position']

    def display_image(self, obj):
        return obj.image.url if obj.image else None

    display_image.short_description = 'Image'


    
    
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


@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')  # Customize the display fields as needed

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')  # Customize the display fields as needed

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')  # Customize the display fields as needed


from .models import Events 

@admin.register(Events)
class EventsAdmin(admin.ModelAdmin):
    list_display = ('name', 'start', 'end')
    search_fields = ('name',)
    list_filter = ('start', 'end')
