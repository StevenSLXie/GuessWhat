#coding:utf-8
from __future__ import absolute_import
from GuessWhat.celery import app
from django.template.loader import get_template
from django.template import Context
from Guess.models import Game, Person, Message, Betting, History, Expertise
from django.core.mail import EmailMultiAlternatives
from django.utils.encoding import smart_text
from datetime import datetime


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
	# need testing in the future
	games = Game.objects.filter(ended = False).order_by('expire')
	now = datetime.now()
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
	# betting = Betting.objects.get(pk=2)  # just a workaround
	for p in persons:
		Message.objects.create(owner=p, betting=None, verbal='你目前的积分是'+str(p.point)+'分, 排名是第'+str(p.rank)+'。')


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


def cal_price():
	# this should be OK as the number of working
	for g in Game.objects.filter(ended=False):
		g.pricing()







