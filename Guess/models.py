#coding:utf-8
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.


class GameTag(models.Model):
	# the type of a game, but a more loose one
	tag = models.CharField(max_length=30)


class PersonTag(models.Model):
	# the expertise of a person
	tag = models.CharField(max_length=30)


class Person(models.Model):
	user = models.OneToOneField(User)
	point = models.IntegerField(default=1000)
	photo = models.FileField(upload_to='%Y/%m/%d/', default= 'cat.jpg')
	expertise = models.ManyToManyField(PersonTag)

	win = models.IntegerField(default=0)
	lose = models.IntegerField(default=0)
	game = models.IntegerField(default=0)
	rank = models.IntegerField(default=0)

	class Meta:
		ordering = ('point', 'win',)


class Game(models.Model):
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

	game_tag = models.ManyToManyField(GameTag)

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
				Message.objects.create(owner=self.better, betting=self, verbal= self._verbal(1))
				self.better.point += 100
				self.better.win += 1
			else:
				self.better.lose += 1
				Message.objects.create(owner=self.better, betting=self, verbal= self._verbal(2))

		else:
			if self.side:
				self.price_at_sell = self.game.price_home
			else:
				self.price_at_sell = self.game.price_away
			self.better.point += self.price_at_sell
			if self.price_at_buy-1 < self.price_at_sell:
				self.better.win += 1
				Message.objects.create(owner=self.better, betting=self, verbal= self._verbal(3))

			else:
				self.better.lose += 1
				Message.objects.create(owner=self.better, betting=self, verbal= self._verbal(4))

		self.cleared = True
		self.better.save()
		self.save()

	def _verbal(self, case):
		s1 = u'竞猜'

		s2 = (self.game.headline)
		if case == 1 or case == 3:
			s3 = u'已结束，你猜对啦，盈利'
		else:
			s3 = u'已结束，你猜错啦，损失'

		if case == 1:
			s4 = str(100-self.price_at_buy)
		elif case == 2:
			s4 = str(self.price_at_buy)
		else:
			s4 = str(abs(self.price_at_sell - self.price_at_buy))

		return s1 + s2 + s3 + s4



class Proposal(models.Model):
	proposer = models.ForeignKey(Person)

	game_type = models.CharField(max_length=30)
	game_cate = models.CharField(max_length=30)  # category, means it is a yes or not qns or a guess figure question
	title = models.CharField(max_length=60)
	content = models.TextField()


class Message(models.Model):
	owner = models.ForeignKey(Person)
	betting = models.ForeignKey(Betting)
	verbal = models.TextField()
	read = models.BooleanField(default=False)


class History(models.Model):
	# the historical price of a game, the home side price, the away side is just 100-home
	cur_price = models.FloatField()
	cur_time = models.DateTimeField()
	game = models.ForeignKey(Game)












