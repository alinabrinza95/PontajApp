"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))
class myForm(forms.Form):
    full_name=forms.CharField(required=True)
    team_leader_email=forms.EmailField(required=True)
    days_off=forms.IntegerField(required=True)

class ConcediuForm(forms.Form):
    #full_name=forms.CharField(required=True)
    #email_address=forms.EmailField(required=True)
    team_leader_name=forms.CharField(required=True)
    start_date=forms.DateField(required=True, widget=forms.TextInput({'placeholder':'YYYY-MM-DD'}))
    end_date=forms.DateField(required=True, widget=forms.TextInput({'placeholder':'YYYY-MM-DD'}))
    days_off=forms.IntegerField(required=True)
    #team_leader_email_address=forms.EmailField(required=True)

class OOHRequestForm(forms.Form):
    day=forms.DateField(required=True, widget=forms.TextInput({'placeholder':'YYYY-MM-DD'}))
    worked_time=forms.IntegerField(required=True)
    incident_number=forms.CharField(required=True)
    #team_leader_email=forms.EmailField(required=True)

class ProfileForm(forms.Form):
    first_name=forms.CharField(required=True)
    last_name=forms.CharField(required=True)
    email_address=forms.EmailField(required=True)
    marca=forms.CharField(required=True)
    CNP=forms.IntegerField(required=True)
    location=forms.CharField(required=True,widget=forms.TextInput({'placeholder':'Iasi/Bacau'}))
    team=forms.CharField(required=True)
    team_leader_email=forms.EmailField(required=True)

class PontajForm(forms.Form):
    marca=forms.CharField(required=True)
    first_name=forms.CharField(required=True)
    last_name=forms.CharField(required=True)
    CNP=forms.CharField(required=True)
    team_leader_email=forms.EmailField(required=True)
    flag=forms.BooleanField(required=True)
