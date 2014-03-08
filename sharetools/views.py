from django.http import HttpResponse
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, get_object_or_404, redirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse

from sharetools.models import Asset, Location, UserProfile, User
from sharetools.forms import LoginForm, UserForm 

def index_view(request):
	if request.user.is_authenticated():
		template = loader.get_template('base_index.html')
		context = RequestContext(request, {
		})
		return HttpResponse(template.render(context))
	else:
		template = loader.get_template('landing.html')
		context = RequestContext(request, {
		})
		return HttpResponse(template.render(context))

def login_view(request):
	if request.user.is_authenticated():
		return redirect('index')
	else:
		if request.method == 'POST':
			form = LoginForm(request.POST)
			if form.is_valid():
				username = form.cleaned_data['username']
				password = form.cleaned_data['password']
				user = authenticate(username=username, password=password)
				if user is not None and user.is_active:
					login(request, user)
					return redirect('index')

			context = RequestContext(request, {
				'login_error': "The username and email you gave us did not match up"
			})
		else:
			context = RequestContext(request, {})

		template = loader.get_template('base_login.html')
		return HttpResponse(template.render(context))

def logout_view(request):
	logout(request)
	return redirect('index')

def register_view(request):
	if request.user.is_authenticated():
		return redirect('index')
	else:
		if request.method == 'POST':
			user_form = UserForm(request.POST)
			# @TODO Check if the user already exist and post good errors
			if user_form.is_valid():
				user = user_from.save()
				# if User.objects.filter(username=user.username, email.user.email).exists():
				profile = UserProfile()
				profile.user = user
				profile.save()
				return redirect('login')

		context = RequestContext(request, {
			'form': UserForm()
		})
		template = loader.get_template('base_register.html')
		return HttpResponse(template.render(context))

def profile_view(request, user_id):
	this_user = get_object_or_404(User, username__iexact=user_id)
	user_profile = this_user.userprofile
	
	template = loader.get_template('base_profile.html')
	context = RequestContext(request, {
		'userProfile': user_profile
	})
	
	return HttpResponse(template.render(context))
	

def shed_view(request, shed_id):
	shedLocation = get_object_or_404(Location, pk=shed_id)
	assets = Asset.objects.filter(location=shedLocation)
	template = loader.get_template('base_shed.html')
	context = RequestContext(request, {
		'location': shedLocation,
		'assets': assets,
	})
	return HttpResponse(template.render(context))

def my_sheds_view(request):
	shedLocations = Location.objects.filter(owner=request.user)
	template = loader.get_template('base_mySheds.html')
	context = RequestContext(request, {
		'shedLocations': shedLocations,
	})
	return HttpResponse(template.render(context))


def my_tools_view(request):
	assets = Asset.objects.filter(owner=request.user)
	template = loader.get_template('base_myTools.html')
	context = RequestContext(request, {
		'assets': assets,
	})
	return HttpResponse(template.render(context))

def tool_view(request, id):
	return HttpResponse("Tool page." + id)

