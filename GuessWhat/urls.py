from django.conf.urls import patterns, include, url
from django.contrib import admin
import notifications
admin.autodiscover()

urlpatterns = patterns('',
	# Examples:
	# url(r'^$', 'GuessWhat.views.home', name='home'),
	# url(r'^blog/', include('blog.urls')),

	url(r'^admin/', include(admin.site.urls)),
	url(r'^$', 'Guess.views.signup', name='signup'),
	url(r'^login$', 'Guess.views.login', name='login'),
	url(r'^home$', 'Guess.views.home', name='home'),
	url(r'^sports$', 'Guess.views.sports', name='sports'),
	url(r'^finance$', 'Guess.views.finance', name='finance'),
	url(r'^profile$', 'Guess.views.profile', name='profile'),
	url(r'^leaderboard$', 'Guess.views.leaderboard', name='leaderboard'),
	url(r'^more$', 'Guess.views.more', name='more'),
	url(r'^logout', 'Guess.views.logout', name='logout'),
	url(r'^proposal$', 'Guess.views.proposal', name='proposal'),
	url(r'^email$', 'Guess.views.email', name='email'),
	url(r'^inbox$', 'Guess.views.inbox', name='inbox'),
	url(r'^ackonwledgement$', 'Guess.views.ack', name='ack')
	# url(r'^user/(?P<index>\d+)/$', 'Guess.views.user_profile', name='user_profile'), # \w+
)
