from django import forms
from django.forms.utils import ErrorList
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from .models import User

from passlib.hash import pbkdf2_sha256
from datetime import date


class ParagraphErrorList(ErrorList):

	def __str__(self):
		return self.as_divs()

	def as_divs(self):
		if not self: return ''
		return '<div class="errorlist">%s</div>' % ''.join(['<p class="text-danger">%s</p>' % e for e in self])

class ContactForm(forms.Form):

	user_first_name = forms.CharField(
		label=_('Your first name'),
		max_length=50,
		required=False,
		widget=forms.TextInput(attrs={'placeholder' : _('Your first name...'),
		 'class' : 'form-control'})
		)

	user_last_name = forms.CharField(
		label=_('Your last name'),
		max_length=50,
		required=False,
		widget=forms.TextInput(attrs={'placeholder' : _('Your last name...'),
		 'class' : 'form-control'})
		)

	user_phone_number = forms.CharField(
		label=_('Your phone number'),
		max_length=30,
		required=False,
		widget=forms.TextInput(attrs={'placeholder' : _('Your phone number...'),
		 'class' : 'form-control'})
		)

	user_email_adress = forms.EmailField(
		label=_('Your email adress (*)'),
		max_length=50,
		required=True,
		widget=forms.EmailInput(attrs={'placeholder' : _('Your email adress...'),
		 'class' : 'form-control'})
		)

	message_subject = forms.CharField(
		label=_('Your message subject (*)'),
		max_length=100,
		required=True,
		widget=forms.TextInput(attrs={'placeholder' : _('Your message subject...'),
		 'class' : 'form-control'})
		)

	message = forms.CharField(
		label=_('Your message (*)'),
		max_length=1000,
		required=True,
		widget=forms.Textarea(attrs={'placeholder' : _('Your message...'),
		 'rows' : 5, 'cols' : 20,
		 'class' : 'form-control'})
		)


class FilterForm(forms.Form):

	age = forms.CharField(
		label=_('Age'),
		max_length=2,
		required=False,
		widget=forms.TextInput(attrs={'placeholder' : _('What age ?'),
		 'class' : 'form-control'})
		)

	player_number = forms.CharField(
		label=_('Player number'),
		max_length=2,
		required=False,
		widget=forms.TextInput(attrs={'placeholder' : _('How many players ?'),
		 'class' : 'form-control'})
		)

	
	def clean_age(self):
		validation = True
		age = self.cleaned_data.get('age')
		
		if age != '':

			try:
				if not age.isnumeric():
					validation = False

				elif int(age) == 0:
					validation = False
					
			except ValueError:
				validation = False

		if validation == False:
			raise forms.ValidationError(_('Age not valid.'))
		
		return age

	def clean_player_number(self):
		validation = True
		player_number = self.cleaned_data.get('player_number')

		if player_number != '':

			try:
				if not player_number.isnumeric():
					validation = False

				elif int(player_number) == 0:
					validation = False

			except ValueError:
				validation = False
		
		if validation == False:
			raise forms.ValidationError(_('Player number not valid.'))

		return player_number


class LogInForm(forms.Form):

	user_login = forms.CharField(
		label=_('Your user login'),
		max_length=30,
		required=True,
		widget=forms.TextInput(attrs={'placeholder' : _('Your user login...'),
		 'class' : 'form-control'})
		)

	user_password = forms.CharField(
		label=_('Your password'),
		max_length=20,
		required=True,
		widget=forms.PasswordInput(attrs={'placeholder' : _('Your password...'),
		 'class' : 'form-control'})
		)

	def clean(self):
		validation = True
		user_login = self.cleaned_data.get('user_login')
		user_password = self.cleaned_data.get('user_password')

		if not User.objects.filter(user_login=user_login).exists():
			validation = False
		
		else:
			try:
				user = User.objects.get(user_login=user_login)
				validation = pbkdf2_sha256.verify(user_password, user.user_password)		
			except:
				validation = False

		if validation == False:
			raise forms.ValidationError(_('The login or the password is wrong.'))

		return self.cleaned_data


class SignUpForm(forms.Form):

	BIRTH_YEAR_CHOICES = list(range(1970, date.today().year))

	user_birth_date = forms.DateField(
		label=_('Your birth date'),
		required=True,
		widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES, attrs={'placeholder' : _('Your birth date...'),
		 'class' : 'form-control'})
		)

	user_email_adress = forms.EmailField(
		label=_('Your email adress'),
		max_length=50,
		required=True,
		widget=forms.TextInput(attrs={'placeholder' : _('Your email adress...'),
		 'class' : 'form-control'})
		)

	user_login = forms.CharField(
		label=_('Your user login'),
		max_length=30,
		required=True,
		widget=forms.TextInput(attrs={'placeholder' : _('Your user login...'),
		 'class' : 'form-control'})
		)

	user_password = forms.CharField(
		label=_('Your password'),
		max_length=20,
		required=True,
		widget=forms.PasswordInput(attrs={'placeholder' : _('Your password...'),
		 'class' : 'form-control'})
		)

	user_password_again = forms.CharField(
		label=_('Your password (again)'),
		max_length=20,
		required=True,
		widget=forms.PasswordInput(attrs={'placeholder' : _('Your password... (again)'),
		 'class' : 'form-control'})
		)

	def clean_user_email_adress(self):
		user_email_adress = self.cleaned_data.get('user_email_adress')

		if User.objects.filter(user_email_adress=user_email_adress).exists():
			raise forms.ValidationError(_('This email adress is already used.'))

		return user_email_adress

	def clean_user_login(self):
		user_login = self.cleaned_data.get('user_login')

		if User.objects.filter(user_login=user_login).exists():
			raise forms.ValidationError(_('This login is already used.'))

		return user_login

	def clean(self):
		user_password = self.cleaned_data.get('user_password')
		user_password_again = self.cleaned_data.get('user_password_again')

		if user_password != user_password_again:
			raise forms.ValidationError(_('The password is not identical in each field.'))

		return self.cleaned_data