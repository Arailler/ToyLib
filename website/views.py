from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import send_mail
from django.db import transaction
from django.utils.translation import gettext as _
from django.utils.translation import get_language

from .models import Game, User, Borrowing
from .forms import ParagraphErrorList, FilterForm, ContactForm, LogInForm, SignUpForm
from toylib.settings import EMAIL_HOST_USER

from datetime import date, datetime
from passlib.hash import pbkdf2_sha256

THIRTY_DAY_TIMESTAMP = 3600 * 24 * 30

# Pages
def about(request):
	context = {}

	if 'user_login' in request.session:
		context['user_login'] = request.session['user_login']
	
	return render(request, 'website/pages/about.html', context)

def contact(request):
	context = {}
	form = ContactForm()
	context['email_sent'] = False

	if request.method == 'POST':
		form = ContactForm(request.POST, error_class=ParagraphErrorList)
		context['form'] = form

		if form.is_valid():

			user_first_name = form.cleaned_data.get('user_first_name')
			user_last_name = form.cleaned_data.get('user_last_name')
			message_subject = form.cleaned_data.get('message_subject')
			user_phone_number = form.cleaned_data.get('user_phone_number')
			user_email_adress = form.cleaned_data.get('user_email_adress')
			message = form.cleaned_data.get('message')

			message += '\n' + '--------------------------------------------'

			if user_first_name != '':
				message += '\n' + 'User first name : ' + user_first_name

			if user_last_name != '':
				message += '\n' + 'User last name : ' + user_last_name
			
			if user_phone_number != '':
				message += '\n' + 'User phone number : ' + user_phone_number

			if user_email_adress != '':
				message += '\n' + 'User email adress : '+ user_email_adress

			send_mail(message_subject,
				message,
				EMAIL_HOST_USER,
				[EMAIL_HOST_USER],
				fail_silently=True)

			context['email_sent'] = True

	else:
		context['form'] = form

	if 'user_login' in request.session:
		context['user_login'] = request.session['user_login']
	
	return render(request, 'website/pages/contact.html', context)

@transaction.atomic
def game_list(request):
	context = {}
	form = FilterForm()

	game_list = Game.objects.all().order_by('-created_at')

	if 'user_login' in request.session:
		user_login = request.session['user_login']
		context['user_login'] = user_login

		user = User.objects.get(user_login=user_login)
		user_adult_date = date(user.user_birth_date.year + 18, user.user_birth_date.month, user.user_birth_date.day)
		
		if user_adult_date > date.today():
			game_list = game_list.filter(game_contains_mature_content=False)

	else:
		game_list = game_list.filter(game_contains_mature_content=False)

	context['form'] = form
	context['game_number'] = game_list.count()
	paginator = Paginator(game_list, 20)
	page = request.GET.get('page')
	
	try:
		game_list = paginator.page(page)
	except PageNotAnInteger:
		game_list = paginator.page(1)
	except EmptyPage:
		game_list = paginator.page(paginator.num_pages)

	context['game_list'] = game_list

	return render(request, 'website/pages/game_list.html', context)

@transaction.atomic
def game_sheet(request, id=None):
	context = {}
	
	game = get_object_or_404(Game, pk=id)
	game.game_number_times_consulted += 1
	
	game.save()
	context['game'] = game

	context['user_borrowing_count'] = len(Borrowing.objects.filter(borrowing_game_id=game.id))
	context['language_code'] = get_language()

	if 'user_login' in request.session:
		context['user_login'] = request.session['user_login']

	return render(request, 'website/pages/game_sheet.html', context)

def index(request):
	context = {}

	if 'user_login' in request.session:
		context['user_login'] = request.session['user_login']
	
	return render(request, 'website/pages/index.html', context)

@transaction.atomic
def log_in(request):
	context = {}
	form = LogInForm()

	if request.method == 'POST':
		form = LogInForm(request.POST, error_class=ParagraphErrorList)

		if form.is_valid():
			user_login = form.cleaned_data.get('user_login')
			request.session['user_login'] = user_login
			return HttpResponseRedirect(reverse('index'))

	context['form'] = form
	
	return render(request, 'website/pages/log_in.html', context)

@transaction.atomic
def sign_up(request):
	context = {}
	form = SignUpForm()
	if request.method == 'POST':
		form = SignUpForm(request.POST, error_class=ParagraphErrorList)

		if form.is_valid():
			user_birth_date = form.cleaned_data.get('user_birth_date')
			user_email_adress = form.cleaned_data.get('user_email_adress')
			user_login = form.cleaned_data.get('user_login')
			user_password = form.cleaned_data.get('user_password')

			user = User()
			user.user_birth_date = user_birth_date
			user.user_email_adress = user_email_adress
			user.user_login = user_login
			user.user_password = user_password
			user.user_password = pbkdf2_sha256.encrypt(user_password, rounds=12000, salt_size=32)
			user.save()

			request.session['user_login'] = user_login
			return HttpResponseRedirect(reverse('index'))

	context['form'] = form
		
	return render(request, 'website/pages/sign_up.html', context)

@transaction.atomic
def user_profile(request, user_login=None):
	context = {}
	
	user = User.objects.get(user_login=user_login)
	context['user'] = user
	context['user_login'] = user.user_login

	all_borrowings_list = Borrowing.objects.filter(borrowing_user_id=user.id)

	temp_all_borrowed_games = []
	temp_current_borrowed_games = []
	temp_all_borrowings = []
	temp_current_borrowings = []
	current_timestamp = datetime.timestamp(datetime.now())
	for borrowing in all_borrowings_list:
		temp_all_borrowed_games.append(Game.objects.get(id=borrowing.borrowing_game_id))
		temp_all_borrowings.append(borrowing)

		if (datetime.timestamp(borrowing.created_at) + THIRTY_DAY_TIMESTAMP) > current_timestamp:
			temp_current_borrowed_games.append(Game.objects.get(id=borrowing.borrowing_game_id))
			temp_current_borrowings.append(borrowing)

	all_borrowed_games_list = zip(temp_all_borrowed_games, temp_all_borrowings)
	current_borrowed_games_list = zip(temp_current_borrowed_games, temp_current_borrowings)

	context['all_borrowed_games_list'] = all_borrowed_games_list
	context['current_borrowed_games_list'] = current_borrowed_games_list

	return render(request, 'website/pages/user_profile.html', context)


# Features
@transaction.atomic
def borrow_game(request, id=None):
	game = get_object_or_404(Game, pk=id)
	user = get_object_or_404(User, user_login=request.session['user_login'])

	if game.game_number_in_stock > 0:

		borrowing = Borrowing()
		borrowing.borrowing_game = Game.objects.get(id=game.id)
		borrowing.borrowing_user = User.objects.get(id=user.id)
		borrowing.borrowing_deadline = datetime.fromtimestamp(datetime.timestamp(datetime.now()) + THIRTY_DAY_TIMESTAMP)
		borrowing.save()

		game.game_number_in_stock -= 1
		game.game_number_times_borrowed += 1
		game.save()

	return redirect('game_sheet', id=id)

def deconnect_user(request):
	if request.session.has_key('user_login'):
		request.session.flush()
		return redirect('index')

@transaction.atomic
def delete_user(request):
	user = User.objects.get(user_login=request.session['user_login'])
	user.delete()
	request.session.flush()
	return redirect('index')

@transaction.atomic
def filter(request):
	context = {}
	game_list = Game.objects.all().order_by('-created_at')
	form = FilterForm(request.GET, error_class=ParagraphErrorList)
	all_game_type_list = ['Board game', 'Card game', 'Construction game', 'Puzzle game', 'Toy', 'Video game']
	active_game_type_list = all_game_type_list

	if form.is_valid():
		active_game_type_list = []

		for i in range(len(all_game_type_list)):
			param = request.GET.get(all_game_type_list[i], 'nan')
		
			if param == 'on' or param == 'default':
				active_game_type_list.append(all_game_type_list[i])

		game_list = game_list.filter(game_type__in=active_game_type_list)
		context['active_game_type_list'] = active_game_type_list

		getURL = '=on&'.join(active_game_type_list)
		getURL= getURL.replace(' ', '+')
		getURL = getURL + '=on'
		
		age = request.GET.get('age', '')
		if age != '':
			game_list = game_list.filter(game_age_min__lte=age, 
				game_age_max__gte=age)

		player_number = request.GET.get('player_number', '')
		if player_number != '':
			game_list = game_list.filter(game_player_number_min__lte=player_number,
				game_player_number_max__gte=player_number)

		getURL = 'age=' + str(age) + '&player_number=' + str(player_number) + '&' + getURL
		context['getURL'] = getURL

	context['form'] = form

	if 'user_login' in request.session:
		user_login = request.session['user_login']
		context['user_login'] = user_login

		user = User.objects.get(user_login=user_login)
		
		user_adult_date = date(user.user_birth_date.year + 18, user.user_birth_date.month, user.user_birth_date.day)
		if user_adult_date > date.today():
			game_list = game_list.filter(game_contains_mature_content=False)

	else:
		game_list = game_list.filter(game_contains_mature_content=False)

	context['game_number'] = game_list.count()
	paginator = Paginator(game_list, 20)
	page = request.GET.get('page')
	
	try:
		game_list = paginator.page(page)
	except PageNotAnInteger:
		game_list = paginator.page(1)
	except EmptyPage:
		game_list = paginator.page(paginator.num_pages)

	context['game_list'] = game_list 

	return render(request, 'website/pages/game_list.html', context)

def search(request):
	context = {}
	form = FilterForm()
	context['form'] = form

	game_list = Game.objects.all().order_by('-created_at')

	research = request.GET.get('research')
	
	if not research or research == "":
		research = "&default"
		
	else:
		game_list = Game.objects.filter(game_name__icontains=research)
	
	context['research'] = research
	
	if 'user_login' in request.session:
		user_login = request.session['user_login']
		context['user_login'] = user_login

		user = User.objects.get(user_login=user_login)
		user_adult_date = date(user.user_birth_date.year + 18, user.user_birth_date.month, user.user_birth_date.day)
		
		if user_adult_date > date.today():
			game_list = game_list.filter(game_contains_mature_content=False)

	else:
		game_list = game_list.filter(game_contains_mature_content=False)

	context['game_number'] = game_list.count()
	paginator = Paginator(game_list, 20)
	
	page = request.GET.get('page')
	
	try:
		game_list = paginator.page(page)
	except PageNotAnInteger:
		game_list = paginator.page(1)
	except EmptyPage:
		game_list = paginator.page(paginator.num_pages)

	context['game_list'] = game_list

	return render(request, 'website/pages/game_list.html', context)