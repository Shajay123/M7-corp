
from django.db import models

from datetime import datetime, time

class TeamMember(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    image = models.ImageField(upload_to='team_member_images/', null=True, blank=True)

    def __str__(self):
        return self.name


class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    Address = models.CharField(max_length=100)
    Pan_Number = models.CharField(max_length=100)
    Aadhar_Number = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    from_time = models.TimeField(null=True, blank=True)
    to_time = models.TimeField(null=True, blank=True)
    

class CheckInOut(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=100)
    check_in_time = models.DateTimeField(auto_now_add=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(upload_to='checkinout_images/', null=True, blank=True)

    def get_username_from_phone_number(self):
        try:
            user = User.objects.get(phone_number=self.phone_number)
            return user.username
        except User.DoesNotExist:
            return None
    
    @classmethod
    def get_username_from_phone_number(self):
        try:
            user = User.objects.get(phone_number=self.phone_number)
            return user.username
        except User.DoesNotExist:
            return "Unknown User"
    


class Hero(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='hero_images')

class Feature(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='feature_images')

class Service(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='service_images')




class Events(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    start = models.DateField(null=True, blank=True)
    end = models.DateField(null=True, blank=True)

    class Meta:
        db_table = "tbevents"

    def save(self, *args, **kwargs):
        if self.start:
            self.start = datetime.combine(self.start, datetime.min.time())
        if self.end:
            self.end = datetime.combine(self.end, datetime.max.time())
        super(Events, self).save(*args, **kwargs)