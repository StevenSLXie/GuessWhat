#coding:utf-8

from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
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
		user = authenticate(username=username, password=password)
	elif request.user.is_authenticated():
		return redirect(reverse('home'))
	else:
		return render(request,'signup_login.html')
	if user is not None:
		if user.is_active:
			auth_login(request,user)
			if not request.POST.get('remember_me', None):
				request.session.set_expiry(0)
			return redirect(reverse('home'))
		else:
			return render(request, 'signup_login.html')
	else:
		return render(request, 'signup_login.html')

def logout(request):
	auth_logout(request)
	return redirect(reverse('login'))



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
		return redirect(reverse('home'))
	else:
		return render(request,'signup.html')


def home(request):
	if not request.user.is_authenticated():
		return redirect(reverse('login'))

	temps = Game.objects.filter(ended=False).order_by('-event','-is_primary')
	gamess = game_choose_and_sort(temps)

	if request.method == 'POST':
		cur_person = Person.objects.get(user=request.user)

		for cur_game in temps:
			accept_bet(request,cur_person,cur_game)

		return redirect(reverse('home'))
	else:
		return render(request, 'home.html', {'gamess': gamess})


def sports(request):
	if not request.user.is_authenticated():
		return redirect(reverse('login'))

	temps = Game.objects.filter(ended=False,game_type='体育').order_by('-event','-is_primary')
	gamess = game_choose_and_sort(temps)

	if request.method == 'POST':
		cur_person = Person.objects.get(user=request.user)

		for cur_game in temps:
			accept_bet(request,cur_person,cur_game)

		return redirect(reverse('sports'))
	else:
		return render(request, 'home.html', {'gamess': gamess})

def finance(request):
	if not request.user.is_authenticated():
		return redirect(reverse('login'))

	temps = Game.objects.filter(ended=False,game_type='财经').order_by('-event','-is_primary')
	gamess = game_choose_and_sort(temps)

	if request.method == 'POST':
		cur_person = Person.objects.get(user=request.user)

		for cur_game in temps:
			accept_bet(request,cur_person,cur_game)

		return redirect(reverse('finance'))
	else:
		return render(request, 'home.html', {'gamess': gamess})

def game_choose_and_sort(temps):
	gamess = []
	games = []
	flag = 0
	for p in temps:
		if flag == 0:
			event = p.event
			flag = 1
		elif p.event != event:
			event = p.event
			gamess.append(games)
			games = []
		games.append(p)

	gamess.append(games)
	return gamess


def accept_bet(request, cur_person,cur_game):
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


def profile(request):
	if not request.user.is_authenticated():
		return redirect(reverse('login'))

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
		return redirect(reverse('profile'))

	else:
		person = Person.objects.get(user=request.user)
		return render(request,'profile.html',{'person': person, 'bets': bets})


def leaderboard(request):
	if not request.user.is_authenticated():
		return redirect(reverse('login'))

	#persons = []
	persons = Person.objects.all().order_by('-point','-win')
	#persons.append(p)
	return render(request,'leaderboard.html',{'persons':persons})

def more(request):
	if not request.user.is_authenticated():
		return redirect(reverse('login'))

	if request.method == 'POST':
		return render(request,'more_info.html')
	else:
		return render(request,'more_info.html')

def proposal(request):
	return render(request, 'proposal.html')

