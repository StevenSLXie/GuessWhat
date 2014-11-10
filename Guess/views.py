from django.shortcuts import render,redirect,render_to_response
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from Guess.models import Person, Game, Betting
from algorithm.data_processing import price_change


# Create your views here.

def login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username,password=password)
	else:
		return render(request,'signup_login.html')
	if user is not None:
		if user.is_active:
			auth_login(request,user)
			if not request.POST.get('remember_me', None):
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
		user = authenticate(username=request.POST['username'],password=request.POST['password'])
		auth_login(request,user)
		return redirect('/home')
	else:
		return render(request,'signup.html')


def home(request):

	para = Game.objects.filter(ended=False)
	if request.method == 'POST':
		cur_person = Person.objects.get(user=request.user)

		for cur_game in Game.objects.filter(ended=False):
			if 'h:'+str(cur_game.pk) in request.POST:
				cur_person.point -= cur_game.price_home
				cur_person.save()
				cur_game.num_home += 1
				cur_game.save()
				Betting.objects.create(better=cur_person, game=cur_game, side=True, num=1, price_at_buy=cur_game.price_home, price_at_sell=cur_game.price_home)
				price_change(cur_game.pk)

			elif 'a:'+str(cur_game.pk) in request.POST:
				cur_person.point -= cur_game.price_away
				cur_person.save()
				cur_game.num_away += 1
				cur_game.save()
				Betting.objects.create(better=cur_person, game=cur_game, side=False, num=1, price_at_buy=cur_game.price_away, price_at_sell=cur_game.price_away)
				price_change(cur_game.pk)

		return redirect('/home')
	else:
		return render(request, 'home.html', {'games': para})


def profile(request):
	person = Person.objects.get(user=request.user)
	bets = []
	for b in Betting.objects.filter(better=person, cleared=False):
		if not b.game.ended:
			bets.append(b)
		else:
			b.clear()
	if request.method == 'POST':
		for b in bets:
			if str(b.pk) in request.POST:
				b.clear()
				break
		return redirect('/profile')

	else:
		person = Person.objects.get(user=request.user)
		return render(request,'profile.html',{'person': person, 'bets': bets})


def leaderboard(request):
	#persons = []
	persons = Person.objects.all()
	#persons.append(p)
	return render(request,'leaderboard.html',{'persons':persons})
