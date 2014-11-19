#coding:utf-8
from __future__ import absolute_import
from GuessWhat.celery import app
from django.template.loader import get_template
from django.template import Context
from Guess.models import Game, Person
from django.core.mail import EmailMultiAlternatives
from django.utils.encoding import smart_text
from email.mime.image import MIMEImage
import os


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
	persons = Person.objects.all().order_by('-point','-win')
	i = 1
	for p in persons:
		p.rank = i
		p.save()
		i += 1

