#coding:utf-8
from __future__ import absolute_import
from GuessWhat.celery import app
from django.template.loader import get_template
from django.template import Context
from Guess.models import Game
from django.core.mail import EmailMultiAlternatives
from django.utils.encoding import smart_text


@app.task
def send_email():
	games = Game.objects.filter(ended=False, is_primary=True).order_by('-event')

	plaintext = get_template('/Users/xingmanjie/Applications/Python/GuessWhat/Guess/templates/email.txt')
	htmly = get_template('/Users/xingmanjie/Applications/Python/GuessWhat/Guess/templates/email.html')
	d = Context({ 'games': games })
	text_content = plaintext.render(d)

	html_content = htmly.render(d)
	html_content = smart_text(html_content)

	SMTP_SERVER = 'smtp.gmail.com'
	SMTP_PORT = 587

	sender = 'stevenslxie@gmail.com'
	recipient = 'stevenslxie@gmail.com'
	subject = '来自Guesso!盖世的每日更新！'

	password = '2xiexing'

	#with open('/Users/xingmanjie/Applications/Python/GuessWhat/Guess/templates/home.html','r') as htmlFile:
	#	body = htmlFile.read().replace('\n','')


	msg = EmailMultiAlternatives(subject, text_content, sender, [recipient])
	msg.attach_alternative(html_content, "text/html")

	msg.send()

'''
	session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

	session.ehlo()
	session.starttls()
	session.ehlo
	session.login(sender, password)

	session.sendmail(sender, recipient, msg.as_string())
	session.quit()

'''