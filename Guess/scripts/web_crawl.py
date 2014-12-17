#coding:utf-8
from bs4 import BeautifulSoup
import requests
import random
import csv
from datetime import datetime
from django.utils import timezone
from Guess.models import Game, Betting, GameTag



def scrapy(url, source):
	# a simple web crawling function to extract info from NetEase Caipiao
	r = requests.get(url)
	data = r.text
	soup = BeautifulSoup(data)


	if source == 'db':
		games = from_net_ease_db(soup)
	elif source == 'everyday':
		games = from_net_ease_every_day(soup)

	# print '456'
	return games


def from_net_ease_every_day(soup):
	games = []

	for link in soup.find_all('dd'):
		j = 0
		game = {}
		flag = True
		for span in link.find_all('span'):

			if j == 2:
				time = span.i['inf'][-16:]
				game['time'] = time
			elif j == 3:
				z = 0
				for em in link.find_all('em'):
					if z == 0:
						home = em['title']
					elif z == 1:
						away = em['title']
					z += 1
				game['home'] = home
				game['away'] = away
			elif j == 4:
				z = 0
				for em in span.div:
					# print span.div
					if z >= 1 and z<=3:
						if not is_float(em.text):
							flag = False
							break
					if z == 2:
						home_price = float(em.text)
						game['home_price'] = home_price
					elif z == 3:
						even_price = float(em.text)
						game['even_price'] = even_price
					elif z == 4:
						away_price = float(em.text)
						game['away_price'] = away_price

					z += 1

				game['result'] = '-'

			j += 1

		if flag and game != {}:
			games.append(game)

	return games


def is_float(s):
	try:
		float(s)
		return True
	except ValueError:
		return False


def from_net_ease_db(soup):
	games = []

	# for link in soup(attrs={'class', 'even'}):
	for link in soup.find_all('tr'):
		i = 0
		game = {}
		for td in link.find_all('td'):
			if i == 0:
				# extract the start time
				time = td.text
				game['time'] = '20' + time
				# print time
			elif i == 1:
				# extract the name of home team
				home = td.a['title']
				game['home'] = home
				# print home
			elif i == 3:
				# extract the name of away team
				away = td.a['title']
				game['away'] = away
				# print away
			elif i == 2:
				# extract the result, if any
				result = td.text
				if not is_number(result[0]):
					game['result'] = '-'
					print '未开赛'
				else:
					game['result'] = result

			elif i == 5:
				# home price
				home_price = float(td.span.text)
				game['home_price'] = home_price
				# print home_price
			elif i == 6:
				# even price
				even_price = float(td.span.text)
				game['even_price'] = even_price
				# print even_price
			elif i == 7:
				# away price
				away_price = float(td.span.text)
				game['away_price'] = away_price
				# print away_price
			i += 1
		if i > 7:
			games.append(game)
		print games
		# print '\n'

	return games


def generate_game_table(url, filename, event, source):
	games = scrapy(url, source)
	with open(filename, 'wb') as file:
		writer = csv.writer(file)
		writer.writerow(['headline','expire','price_home','price_away','weight_home','weight_away','event','is_primary','game_tag','result'])
		for g in games:
			print g
			headline = g['home'] + word_shuffle() + g['away']
			expire = g['time']
			price_home, price_away, weight_home, weight_away = pricing(g['home_price'], g['away_price'], g['even_price'])
			writer.writerow([headline.encode('utf-8'), expire, price_home, price_away, weight_home, weight_away, event, 1, u'体育'.encode('utf-8'), g['result']])
			event += 1
	return event


def add_games(filename):
	with open(filename) as csvfile:
		reader = csv.DictReader(csvfile)
		for r in reader:
			time =timezone.make_aware(datetime.strptime(r['expire'], "%Y-%m-%d %H:%M"), timezone.get_default_timezone())
			if time > timezone.make_aware(datetime.now(), timezone.get_default_timezone()):
				g = Game.objects.create(
					headline=r['headline'], expire=time, price_home=int(r['price_home']), price_away=int(r['price_away']),
					name_home='赞同', name_away='反对', weight_home=int(r['weight_home']), weight_away=int(r['weight_away']), event=int(r['event']), is_primary=int(r['is_primary']))
				t = GameTag.objects.get(tag=r['game_tag'])
				g.game_tag.add(t)
				g.save()
				print g.headline


def scan_game_result(filename):
	with open(filename) as csvfile:
		reader = csv.DictReader(csvfile)
		for r in reader:
			if is_number(r['result'][0]):
				# ideally there should be only one game
				games = Game.objects.filter(event=r['event'], ended=True)
				if games is not None:
					for g in games:
						if int(r['result'][0]) > int(r['result'][2]):
							g.outcome = True
						g.save()
						bets = g.betting_set.filter(cleared=False)
						for b in bets:
							b.clear()


def pricing(home, away, even=0.0):
	# determine the price based on prior information
	sum = home + away + even
	home_price = int((away+even)/sum*100)
	away_price = 100-home_price

	home_weight = 2*home_price
	away_weight = 2*away_price

	return home_price, away_price, home_weight, away_weight


def word_shuffle():
	words = [u'将击败',u'会赢', u'能击败', u'能赢', u'肯定能击败', u'可以击败']
	r = random.randint(0, len(words)-1)
	return words[r]

def is_number(s):
	try:
		int(s)
		return True
	except ValueError:
		return False
