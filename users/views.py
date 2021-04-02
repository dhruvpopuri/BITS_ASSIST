from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from users.models import Profile
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm, UserUpdateForm
from django.contrib import messages
from allauth.socialaccount.models import SocialAccount
from bs4 import BeautifulSoup
from urllib.request import urlopen


# Create your views here.
@login_required
def myprofile(request):
	user = request.user
	profile = Profile.objects.get(user=user)
	
	account = SocialAccount.objects.get(user=user)
	extra_data = account.extra_data
	user_email = extra_data['email']
	profile.image_url = extra_data['picture']
	profile.email = user_email

	profile.save()

	if request.method == "POST":
		u_form = UserUpdateForm(request.POST,instance=request.user)	
		p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)

		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			
			return redirect('myprofile')


	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)

	
	image_url = profile.image_url
	image = profile.image


	




	context={
		'u_form':u_form,
		'p_form':p_form,
		'user_email':user_email,
		'image_url':image_url,
		'image':image,
	}



	return render(request,'users/myprofile.html',context)