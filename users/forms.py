from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from django import forms

class ProfileUpdateForm(forms.ModelForm):

	class Meta:
		model = Profile
		fields = ['email','bio','image']



class UserUpdateForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username']


