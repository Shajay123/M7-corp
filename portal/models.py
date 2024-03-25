
from django.db import models


class TeamMember(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    image = models.ImageField(upload_to='team_member_images/', null=True, blank=True)

    def __str__(self):
        return self.name


class LeaveRequest(models.Model):

    id = models.BigAutoField(primary_key=True) 
    
    leave_type = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)  # Allow end_date to be null for certain leave types
    start_time = models.TimeField(null=True, blank=True)  # For Permission leave type
    end_time = models.TimeField(null=True, blank=True)  # For Permission leave type
    description = models.TextField()

    def __str__(self):
        if self.leave_type == 'Permission':
            return f'{self.leave_type} - {self.start_date} {self.start_time} to {self.end_date} {self.end_time}'
        else:
            return f'{self.leave_type} - {self.start_date}'
        
class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    Address = models.CharField(max_length=100)
    Pan_Number = models.CharField(max_length=100)
    Aadhar_Number = models.CharField(max_length=100)
    Phone_Number = models.CharField(max_length=100)
    from_time = models.TimeField(null=True, blank=True)
    to_time = models.TimeField(null=True, blank=True)