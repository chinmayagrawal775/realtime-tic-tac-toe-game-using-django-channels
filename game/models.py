from django.db import models
import json

# Create your models here.
class Game(models.Model):
    game_code = models.CharField(max_length=6)
    game_creator = models.CharField(max_length=50)
    game_opponent = models.CharField(max_length=50, default='to-be-decided')
    game_matrix = models.ForeignKey("GameMatrix", on_delete=models.CASCADE)

class GameMatrix(models.Model):
    game_code = models.CharField(max_length=6)
    matrix_map = models.CharField(max_length=50, default="[1,2,3,4,5,6,7,8,9]")

    def get_map(self):
        return json.loads(self.matrix_map)