from Guess.models import Game


def price_change(primary_key):
	game = Game.objects.get(pk=primary_key)
	game.price_home = game.num_home/(game.num_home+game.num_away+0.1)*100
	game.price_away = 100-game.price_home
	game.save()