#coding:utf-8
from __future__ import absolute_import
from GuessWhat.celery import app
from django.template.loader import get_template
from django.template import Context
from Guess.models import Game, Person, Message, Betting, History, Expertise, GameTag
from django.core.mail import EmailMultiAlternatives
from django.utils.encoding import smart_text
from datetime import datetime
import csv
from django.utils import timezone


@app.task
def send_email():
	games = Game.objects.filter(ended=False, is_primary=True).order_by('-event')
	person = Person.objects.get(pk=1)

	plaintext = get_template('/Users/xingmanjie/Applications/Python/GuessWhat/Guess/templates/email.txt')
	htmly = get_template('/Users/xingmanjie/Applications/Python/GuessWhat/Guess/templates/email2.html')
	d = Context({ 'games': games, 'person':person })
	text_content = plaintext.render(d)

	html_content = htmly.render(d)
	html_content = smart_text(html_content)


	sender = 'stevenslxie@gmail.com'
	recipient = 'stevenslxie@gmail.com'
	subject = '来自Guesso!盖世的每日更新！'

	msg = EmailMultiAlternatives(subject, text_content, sender, [recipient, '226787208@qq.com' ])
	msg.attach_alternative(html_content, "text/html")

	msg.send()

	image_dir = '/Users/xingmanjie/Applications/Python/GuessWhat/Guess/static/images'


@app.task
def ranking():
	# tested
	persons = Person.objects.all().order_by('-point','-win')
	i = 1
	for p in persons:
		p.rank = i
		p.save()
		i += 1


@app.task
def detect_ended_game():
	# partially tested.
	games = Game.objects.filter(ended=False).order_by('expire')
	# now = datetime.now()
	now = timezone.make_aware(datetime.now(), timezone.get_default_timezone())
	for g in games:
		if g.expire > now:
			break
		else:
			g.ended = True
			g.save()

@app.task
def send_profile_to_inbox():
	# tested
	persons = Person.objects.all()
	betting = Betting.objects.get(pk=2)  # just a workaround
	for p in persons:
		Message.objects.create(owner=p, betting=betting, verbal='你目前的积分是'+str(p.point)+'分, 排名是第'+str(p.rank)+'。')


@app.task
def record_history_data():
	# partially tested, need to see how it run in the periodic mode
	games = Game.objects.filter(ended=False)
	for g in games:
		History.objects.create(cur_price=g.price_home, cur_time=datetime.now(), game=g)


@app.task
def cal_expertise():
	# need to optimise; cannot execute on all users at one time
	for p in Person.objects.all():
		for t in p.expertise.all():
			e = Expertise.objects.get(expert=p, tag=t)
			e.evaluate()

@app.task
def add_expertise():
	for p in Person.objects.all():
		for t in GameTag.objects.all():
			e = Expertise.objects.get_or_create(expert=p, tag=t)

@app.task
def update_expertise():
	# !!! one time use ONLY !
	for e in Expertise.objects.all():
		e.score = 10
		e.save()


@app.task
def add_game_weight():
	# !!! just for one time use. To initialize the point of each game;
	for g in Game.objects.filter(ended=False):
		g.weight_home += 100
		g.weight_away += 100
		g.save()


@app.task
def add_games(file_name):
	with open(file_name) as csvfile:
		reader = csv.DictReader(csvfile)
		for r in reader:
			time =timezone.make_aware(datetime.strptime(r['expire'], "%Y-%m-%d %H:%M:%S"), timezone.get_default_timezone())
			if time > timezone.make_aware(datetime.now(), timezone.get_default_timezone()):
				g = Game.objects.create(
					headline=r['headline'], expire=time, price_home=int(r['price_home']), price_away=int(r['price_away']),
					name_home='赞同', name_away='反对', weight_home=int(r['weight_home']), weight_away=int(r['weight_away']), event=int(r['event']), is_primary=int(r['is_primary']))
				t = GameTag.objects.get(tag=r['game_tag'])
				g.game_tag.add(t)
				g.save()
				print g.headline














