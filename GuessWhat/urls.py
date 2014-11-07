from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'GuessWhat.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
	url(r'^$','Guess.views.login',name='login'),
	url(r'^signup','Guess.views.signup',name='signup'),
	url(r'^home','Guess.views.home',name='home'),
)
