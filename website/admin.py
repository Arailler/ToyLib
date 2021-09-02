from django.contrib import admin

from .models import Game, User, Borrowing

admin.site.register(Game)
admin.site.register(User)
admin.site.register(Borrowing)