#coding：utf-8
from django.db.models.signals import post_save
from notifications import notify
from Guess.models import Betting

def my_handler(sender, instance, created, **kwargs):
    notify.send(instance, verb='已清算')

post_save.connect(my_handler, sender=Betting)