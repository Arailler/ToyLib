from django.conf.urls import url

from . import views

urlpatterns = [

	# Pages
	url(r'^$', views.index, name='index'),
	url(r'^about/$', views.about, name='about'),
	url(r'^contact/$', views.contact, name='contact'),
    url(r'^game_list/$', views.game_list, name='game_list'),
    url(r'^game_sheet/(?P<id>[0-9]+)$', views.game_sheet, name='game_sheet'),
    url(r'^log_in/$', views.log_in, name='log_in'),
    url(r'^sign_up/$', views.sign_up, name='sign_up'),
    url(r'^user_profile/(?P<user_login>[a-zA-Z0-9_-]+)$', views.user_profile, name='user_profile'),

	# Features
	url(r'^borrow_game/(?P<id>[0-9]+)$', views.borrow_game, name='borrow_game'),
	url(r'^deconnect_user/$', views.deconnect_user, name='deconnect_user'),
	url(r'^delete_user/$', views.delete_user, name='delete_user'),
	url(r'^filter/$', views.filter, name='filter'),
	url(r'^search/$', views.search, name='search')
	]