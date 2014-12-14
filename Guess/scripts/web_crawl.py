#coding:utf-8
from bs4 import BeautifulSoup
import requests
import random
import csv


def scrapy(url):
	# a simple web crawling function to extract info from NetEase Caipiao
	r = requests.get(url)
	data = r.text
	soup = BeautifulSoup(data)

	games = []

	# for link in soup(attrs={'class', 'even'}):
	for link in soup.find_all('tr'):
		i = 0
		game = {}
		for td in link.find_all('td'):
			if i == 0:
				# extract the start time
				time = td.text
				game['time'] = time
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
		if i > 0:
			games.append(game)
		print games
		# print '\n'

	return games


def generate_table(url, filename):
	games = scrapy(url)
	with open(filename, 'a') as file:
		writer = csv.writer(file)
		i = 30
		for g in games:
			print g
			headline = g['home'] + word_shuffle() + g['away']
			expire = '20' + g['time'] + ':00'
			price_home, price_away, weight_home, weight_away = pricing(g['home_price'], g['away_price'], g['even_price'])
			writer.writerow([headline.encode('utf-8'), expire, price_home, price_away, weight_home, weight_away, i, 1, u'体育'.encode('utf-8')])
			i += 1


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