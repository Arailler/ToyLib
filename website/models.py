from django.db import models

class ModificationHistory(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True

class Game(ModificationHistory):
	game_age_min = models.IntegerField()
	game_age_max = models.IntegerField()
	game_contains_mature_content = models.BooleanField()
	game_description_de = models.TextField()
	game_description_en = models.TextField()
	game_description_es = models.TextField()
	game_description_fr = models.TextField()
	game_description_pt = models.TextField()
	game_image_path = models.CharField(max_length=100)
	game_name = models.CharField(max_length=80)
	game_number_in_stock = models.IntegerField()
	game_number_times_consulted = models.IntegerField()
	game_number_times_borrowed = models.IntegerField()
	game_player_number_min = models.IntegerField()
	game_player_number_max = models.IntegerField()
	game_type = models.CharField(max_length=50)

	def __str__(self):
		return self.game_name


class User(ModificationHistory):
	user_birth_date = models.DateField()
	user_email_adress = models.CharField(max_length=50)
	user_login = models.CharField(max_length=30)
	user_password = models.CharField(max_length=150)

	def __str__(self):
		return self.user_login


class Borrowing(ModificationHistory):
	borrowing_game = models.ForeignKey(Game, on_delete=models.CASCADE)
	borrowing_user = models.ForeignKey(User, on_delete=models.CASCADE)
	borrowing_deadline = models.DateTimeField()

	def __str__(self):
		return "{} - {} - {}".format(self.borrowing_game.game_name,
			self.borrowing_user.user_login,
			self.borrowing_deadline.strftime("%m/%d/%Y, %H:%M:%S"))