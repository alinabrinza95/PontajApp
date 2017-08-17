"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Concediu(models.Model):
    full_name=models.CharField(max_length=100)
    email_address=models.EmailField(max_length=100)
    team_leader_name=models.CharField(max_length=100)
    start_date=models.DateField(max_length=100)
    end_date=models.DateField(max_length=100)
    days_off=models.IntegerField()
    team_leader_email_address=models.EmailField(max_length=100)
    flag=models.BooleanField(default=False)

class Profile(models.Model):
    username=models.CharField(max_length=100)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email_address=models.EmailField(max_length=100)
    marca=models.IntegerField()
    CNP=models.CharField(max_length=13)
    location=models.CharField(max_length=100)
    team=models.CharField(max_length=100)
    team_leader_email=models.EmailField(max_length=100)

class Pontaj(models.Model):
    marca=models.CharField(max_length=4)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    CNP=models.CharField(max_length=13)
    team_leader_email=models.EmailField(max_length=100)
    flag=models.BooleanField(default=False)

class OOHRequest(models.Model):
    full_name=models.CharField(max_length=100)
    day=models.DateField(max_length=100)
    worked_time=models.IntegerField(blank=False)
    incident_number=models.CharField(max_length=100)
    team_leader_email=models.EmailField(max_length=100)
    flag=models.BooleanField(default=False)


