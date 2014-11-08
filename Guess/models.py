from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Person(models.Model):
	user = models.OneToOneField(User)
	point = models.IntegerField(default=1000)
	# photo = models.ImageField(max_length=1000)
	expertise = models.TextField(default='N/A')

	win = models.IntegerField(default=0)
	lose = models.IntegerField(default=0)
	game = models.IntegerField(default=0)

	point_per_game = models.FloatField(default=0.0)


	class Meta:
		ordering = ('point','point_per_game',)


class Game(models.Model):
	index = models.IntegerField()
	headline = models.TextField()
	begin = models.DateTimeField()
	expire = models.DateTimeField()

	price_home = models.IntegerField(default=50)
	num_home = models.IntegerField(default=0)
	price_away = models.IntegerField(default=50)
	num_away = models.IntegerField(default=0)

	outcome = models.BooleanField()   # True means home wins and vice versa

	# better = models.ManyToManyField(Person,related_name='better')

	class Meta:
		ordering = ('expire',)


class Betting(models.Model):
	better = models.ForeignKey(Person)
	game = models.ForeignKey(Game)
	side = models.BooleanField()  # True means home wins and vice versa
	num = models.IntegerField(default=1)
	price_at_buy = models.FloatField()




