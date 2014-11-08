from django.contrib import admin
from Guess.models import Game, Person, Betting

# Register your models here.
admin.site.register(Game)
admin.site.register(Person)
admin.site.register(Betting)