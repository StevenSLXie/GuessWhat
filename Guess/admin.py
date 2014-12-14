from django.contrib import admin
from Guess.models import Game, Person, Betting, Proposal, PersonTag, GameTag, Message, Expertise, Comments

# Register your models here.

class GameAdmin(admin.ModelAdmin):
	list_display = ('headline', 'expire', 'ended')

admin.site.register(Game, GameAdmin)
admin.site.register(Person)
admin.site.register(Betting)
admin.site.register(Proposal)
admin.site.register(PersonTag)
admin.site.register(GameTag)
admin.site.register(Message)
admin.site.register(Expertise)
admin.site.register(Comments)