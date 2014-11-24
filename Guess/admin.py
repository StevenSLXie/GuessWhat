from django.contrib import admin
from Guess.models import Game, Person, Betting, Proposal, PersonTag, GameTag, Message

# Register your models here.
admin.site.register(Game)
admin.site.register(Person)
admin.site.register(Betting)
admin.site.register(Proposal)
admin.site.register(PersonTag)
admin.site.register(GameTag)
admin.site.register(Message)