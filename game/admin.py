from django.contrib import admin
from .models import Game, GameMatrix

# Register your models here.
@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['id', 'game_code', 'game_creator', 'game_opponent', 'game_matrix']

@admin.register(GameMatrix)
class GameAdmin(admin.ModelAdmin):
    list_display = ['id', 'game_code', 'matrix_map']