from django.shortcuts import render,redirect,render_to_response
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from Guess.models import Person,Game


# Create your views here.

def login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username,password=password)
	else:
		# return render(request, 'login.html')
		return render(request,'signup_login.html')
	if user is not None:
		if user.is_active:
			auth_login(request,user)
			if not request.POST.get('remember_me',None):
				request.session.set_expiry(0)

			return redirect('/home')
		else:
			return render(request, 'signup_login.html')
	else:
		return render(request, 'signup_login.html')


def signup(request):
	if request.method == 'POST':
		if (not request.POST['email']) or (not request.POST['username']) or (not request.POST['password']) or (not request.POST['password_confirm']):
			return render(request,'signup.html')
		elif request.POST['password'] != request.POST['password_confirm']:
			return render(request,'signup.html')

		User.objects.create_user(request.POST['username'],request.POST['email'],request.POST['password'])
		cur_user = User.objects.get(username=request.POST['username'])
		Person.objects.create(user=cur_user)
		return redirect('/home')
	else:
		return render(request,'signup.html')

def home(request):
	return render(request,'home.html')
