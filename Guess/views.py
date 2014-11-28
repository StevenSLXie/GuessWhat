#coding:utf-8

from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from Guess.models import Person, Game, Betting, Proposal, Message, GameTag
from Guess.form import ImageForm
from algorithm.data_processing import price_change
import random


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
	if request.user.is_authenticated():
		return redirect(reverse('home'))

	games = Game.objects.filter(ended=False, is_primary=1)
	r = random.randint(0,len(games)-1)
	game = games[r]

	if request.method == 'POST':
		if 'shuffle' in request.POST:
			return render(request, 'signup.html')
		#if 'i_have_an_account' in request.POST:
		#	print 1
		#	render(request, 'signup_login.html')
		if (not request.POST['email']) or (not request.POST['username']) or (not request.POST['password']) or (not request.POST['password_confirm']):
			return render(request, 'signup.html')
		elif request.POST['password'] != request.POST['password_confirm']:
			return render(request, 'signup.html')

		User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
		cur_user = User.objects.get(username=request.POST['username'])
		Person.objects.create(user=cur_user)
		user = authenticate(username=request.POST['username'],password=request.POST['password'])
		auth_login(request,user)
		return redirect(reverse('home'))
	else:
		return render(request, 'signup.html', {'game':game})

def marked_all_as_read(person):
	for m in Message.objects.filter(owner=person, read=False):
		m.read = True
		m.save()

def render_main(request, url, game_type=None):
	if not request.user.is_authenticated():
		return redirect(reverse('login'))

	if game_type is None:
		temps = Game.objects.filter(ended=False).order_by('-event','-is_primary')
	else:
		# temps = Game.objects.filter(ended=False,game_type=game_type).order_by('-event','-is_primary')
		temps = Game.objects.filter(ended=False, game_tag__tag=game_type).order_by('-event', '-is_primary')
	gamess = game_choose_and_sort(temps)
	cur_person = Person.objects.get(user=request.user)

	if request.method == 'POST':
		if 'marked_all_as_read' in request.POST:
			marked_all_as_read(cur_person)

		for cur_game in temps:
			accept_bet(request, cur_person, cur_game)

		return redirect(reverse(url)+'#success')
	else:
		para = {}
		para['gamess'] = gamess
		para = encap_para(para, cur_person)
		return render(request, 'home.html', para)



def home(request):
	return render_main(request, 'home')


def sports(request):
	return render_main(request, 'sports', '体育')


def finance(request):
	return render_main(request, 'finance', '财经')


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
		b = Betting.objects.create(better=cur_person, game=cur_game, side=True, num=1, price_at_buy=cur_game.price_home, price_at_sell=cur_game.price_home)
		# price_change(cur_game.pk)
		cur_game.pricing(b,cur_person)
	elif 'a:'+str(cur_game.pk) in request.POST:
		cur_person.point -= cur_game.price_away
		cur_person.save()
		cur_game.num_away += 1
		cur_game.save()
		b = Betting.objects.create(better=cur_person, game=cur_game, side=False, num=1, price_at_buy=cur_game.price_away, price_at_sell=cur_game.price_away)
		# price_change(cur_game.pk)
		cur_game.pricing(b,cur_person)


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

		if 'marked_all_as_read' in request.POST:
			marked_all_as_read(person)

		if 'sell_all' in request.POST:
			for b in bets:
				b.clear()
		elif 'sell_win_bets' in request.POST:
			for b in bets:
				if b.side and b.game.price_home > b.price_at_buy:
					b.clear()
				elif (not b.side) and b.game.price_away > b.price_at_buy:
					b.clear()
		else:
			for b in bets:
				if str(b.pk) in request.POST:
					b.clear()
					break


		return redirect(reverse('profile'))

	else:
		person = Person.objects.get(user=request.user)
		para = {}
		para['person'] = person
		para['bets'] = bets
		para = encap_para(para, person)

		return render(request, 'profile.html', para)

def find_unread(person):
	return person.message_set.filter(read=False)


def leaderboard(request):
	if not request.user.is_authenticated():
		return redirect(reverse('login'))

	cur_person = Person.objects.get(user=request.user)
	persons = Person.objects.all().order_by('rank','-point','-win')

	para = {}
	para['persons'] = persons
	para = encap_para(para, cur_person)
	return render(request,'leaderboard.html',para)


def more(request):
	if not request.user.is_authenticated():
		return redirect(reverse('login'))

	person = Person.objects.get(user=request.user)
	form = ImageForm(request.POST, request.FILES)
	if request.method == 'POST':

		if form.is_valid():
			person.photo = request.FILES['image']
			person.save()
		return redirect(reverse('more'))

	else:
		para = {}
		para =encap_para(para, person)
		para['person'] = person
		para['form'] = form
		return render(request, 'more_info.html', para)



def proposal(request):
	proposer = Person.objects.get(user=request.user)
	if request.method == 'POST':
		if 'marked_all_as_read' in request.POST:
			marked_all_as_read(proposer)
		else:
			title = request.POST['title']
			content = request.POST['content']
			game_type = request.POST['type_select']
			game_cate = request.POST['cate_select']
			Proposal.objects.create(proposer=proposer, title=title, content=content, game_type=game_type, game_cate=game_cate)
		return redirect(reverse('home'))

	else:
		para = {}
		para = encap_para(para, proposer)
		return render(request, 'proposal.html', para)


def encap_para(para, person):
	messages = find_unread(person)
	para['messages'] = messages
	para['person'] = person
	return para


def email(request):
	games = Game.objects.filter(ended=False, is_primary=True).order_by('-event')
	person = Person.objects.get(pk=1)
	return render(request, 'email2.html', {'person':person, 'games': games})


def inbox(request):
	para = {}
	person = Person.objects.get(user=request.user)
	messages = Message.objects.filter(owner=person, read=False)
	if request.method == "POST":
		if 'marked_all_as_read' in request.POST:
			marked_all_as_read(person)
		else:
			for m in messages:
				if str(m.pk) in request.POST:
					m.read = True
					m.save()
					break

	para = encap_para(para, person)
	return render(request, 'inbox.html', para)


def ack(request):
	para = {}
	person = Person.objects.get(user=request.user)
	para = encap_para(para, person)
	return render(request, 'ack.html', para)
