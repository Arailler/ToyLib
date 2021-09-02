from django.test import TestCase
from django.urls import reverse

# Pages
class PagesTestCase(TestCase):
	def test_index_page(self):
		response = self.client.get(reverse('index'))
		self.assertEqual(response.status_code, 200)

	def test_about_page(self):
		response = self.client.get(reverse('about'))
		self.assertEqual(response.status_code, 200)

	def test_contact_page(self):
		response = self.client.get(reverse('contact'))
		self.assertEqual(response.status_code, 200)

	def test_game_list_page(self):
		response = self.client.get(reverse('game_list'))
		self.assertEqual(response.status_code, 200)

	def test_log_in_page(self):
		response = self.client.get(reverse('log_in'))
		self.assertEqual(response.status_code, 200)

	def test_sign_up_page(self):
		response = self.client.get(reverse('sign_up'))
		self.assertEqual(response.status_code, 200)