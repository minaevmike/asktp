from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'askminaev.views.home', name='home'),
    # url(r'^askminaev/', include('askminaev.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
	#url(r'^admin/', include(admin.site.urls)),
	#url(r'^aaa/', include('ask.urls')),
	url(r'^$', 'ask.views.index'),
	url(r'^search/$', 'ask.views.search'),
	url(r'^user/$', 'ask.views.user'),
	url(r'^right/$', 'ask.views.righta'),
	url(r'^register/$', 'ask.views.register'),
	url(r'^like/$', 'ask.views.like'),
	url(r'^dislike/$', 'ask.views.dislike'),
	url(r'^alike/$', 'ask.views.alike'),
	url(r'^adislike/$', 'ask.views.adislike'),
	url(r'^login/$', 'ask.views.login_user'),
	url(r'^logout/$', 'ask.views.logout_user'),
	url(r'^answers/$', 'ask.views.answers'),
	url(r'^ask/$', 'ask.views.ask'),
	url(r'^answer/$', 'ask.views.answer'),
	url(r'^ans/$', 'ask.views.ans'),
	url(r'^popular/$', 'ask.views.popular'),
)

