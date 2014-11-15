#coding:utf-8

from __future__ import absolute_import
from GuessWhat.celery import app
import smtplib


@app.task
def add(x, y):
	return x + y

@app.task
def mul(x, y):
	return x * y


@app.task
def xsum(numbers):
	return sum(numbers)

@app.task
def send_email():
	SMTP_SERVER = 'smtp.gmail.com'
	SMTP_PORT = 587

	sender = 'stevenslxie@gmail.com'
	password = '2xiexing'
	recipient = 'stevenslxie@gmail.com'
	subject = 'Guesso! 盖世的第一封测试电邮！'
	body = '愿这是一个美好的开始。'

	headers = ["From: " + sender,
			   "Subject: " + subject,
			   "To: " + recipient,
			 "MIME-Version: 1.0",
			 "Content-Type: text/html"]
	headers = "\r\n".join(headers)

	session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

	session.ehlo()
	session.starttls()
	session.ehlo
	session.login(sender, password)

	session.sendmail(sender, recipient, headers + "\r\n\r\n" + body)
	session.quit()