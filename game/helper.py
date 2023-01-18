from .models import Game, GameMatrix
from channels.db import database_sync_to_async
import json

@database_sync_to_async
def setup_game(game_code, game_matrix_id, player_name, player_type):

    game_matrix =GameMatrix.objects.get(id=game_matrix_id)    

    if(player_type == 'null'):
        game = Game.objects.create(game_code=game_code, game_creator=player_name, game_matrix=game_matrix)
        game.save()
        return game.id

    elif(player_type == 'on'):
        game = Game.objects.update(game_code=game_code, game_opponent=player_name)
        return game

@database_sync_to_async
def update_matrix(matrix_id, box_id, player_type):

    game_matrix_map = GameMatrix.objects.get(id=matrix_id).get_map()
    box_id = int(box_id) - 1

    if(player_type == 'null'):
        game_matrix_map[box_id] = 44
    elif(player_type == 'on'):
        game_matrix_map[box_id] = 11

    updated_matrix_map = json.dumps(game_matrix_map)
    GameMatrix.objects.filter(id=matrix_id).update(matrix_map=updated_matrix_map)

@database_sync_to_async
def check_winner(matrix_id):

    base_map = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    gm_map = GameMatrix.objects.get(id=matrix_id).get_map()
    
    if( (gm_map[0] == gm_map[1] == gm_map[2] == 11) or (gm_map[3] == gm_map[4] == gm_map[5] == 11) or (gm_map[6] == gm_map[7] == gm_map[8] == 11) ):
        return 11
    elif( (gm_map[0] == gm_map[1] == gm_map[2] == 44) or (gm_map[3] == gm_map[4] == gm_map[5] == 44) or (gm_map[6] == gm_map[7] == gm_map[8] == 44) ): 
        return 44
    elif( (gm_map[0] == gm_map[3] == gm_map[6] == 11) or (gm_map[1] == gm_map[4] == gm_map[7] == 11) or (gm_map[2] == gm_map[5] == gm_map[8] == 11) ):
        return 11
    elif( (gm_map[0] == gm_map[3] == gm_map[6] == 44) or (gm_map[1] == gm_map[4] == gm_map[7] == 44) or (gm_map[2] == gm_map[5] == gm_map[8] == 44) ):
        return 44
    elif( (gm_map[0] == gm_map[4] == gm_map[8] == 11) or (gm_map[2] == gm_map[4] == gm_map[6] == 11) ):
        return 11
    elif( (gm_map[0] == gm_map[4] == gm_map[8] == 44) or (gm_map[2] == gm_map[4] == gm_map[6] == 44) ):
        return 44
    else:
        return any(element in gm_map for element in base_map)