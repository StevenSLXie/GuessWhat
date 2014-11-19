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

	index = models.IntegerField(default=0)
	rank = models.IntegerField(default=0)


	class Meta:
		ordering = ('point','point_per_game',)


class Game(models.Model):
	index = models.IntegerField()
	headline = models.TextField()
	begin = models.DateTimeField(auto_now_add=True)
	expire = models.DateTimeField()

	name_home = models.CharField(max_length=30)
	price_home = models.IntegerField(default=50)
	num_home = models.IntegerField(default=0)
	name_away = models.CharField(max_length=30)
	price_away = models.IntegerField(default=50)
	num_away = models.IntegerField(default=0)

	outcome = models.BooleanField(default=False)   # True means home wins and vice versa

	ended = models.BooleanField(default=False)

	event = models.IntegerField()
	is_primary = models.IntegerField(default=0)

	game_type = models.CharField(max_length=50)

	class Meta:
		ordering = ('expire',)


class Betting(models.Model):
	better = models.ForeignKey(Person)
	game = models.ForeignKey(Game)

	side = models.BooleanField()  # True means home wins and vice versa
	num = models.IntegerField(default=1)
	outcome = models.BooleanField(default=False)

	price_at_buy = models.FloatField()
	price_at_sell = models.FloatField()

	# end_when_clear = models.BooleanField(default=False) # when the bet is clear, is the game over?
	cleared = models.BooleanField(default=False)  # cleared means the result of the betting has been updated to the person profile

	def clear(self):
		# clear this deal when game over or when the player ends the game earlier.
		if self.game.ended:
			if self.side == self.outcome:
				self.better.point += 100
				self.better.win += 1
			else:
				self.better.lose += 1

		else:
			if self.side:
				self.price_at_sell = self.game.price_home
			else:
				self.price_at_sell = self.game.price_away
			self.better.point += self.price_at_sell
			if self.price_at_buy-1 < self.price_at_sell:
				self.better.win += 1
			else:
				self.better.lose += 1

		self.cleared = True
		self.better.save()
		self.save()


class Proposal(models.Model):
	proposer = models.ForeignKey(Person)

	game_type = models.CharField(max_length=30)
	game_cate = models.CharField(max_length=30)  # category, means it is a yes or not qns or a guess figure question
	title = models.CharField(max_length=60)
	content = models.TextField()


class Message(models.Model):
	owner = models.ForeignKey(Person)
	betting = models.ForeignKey(Betting)
	verbal = models.CharField(max_length=300)
	read = models.BooleanField(default=False)

class History(models.Model):
	# the historical price of a game, the home side price, the away side is just 100-home
	cur_price = models.FloatField()
	cur_time = models.DateTimeField()
	game = models.ForeignKey(Game)











