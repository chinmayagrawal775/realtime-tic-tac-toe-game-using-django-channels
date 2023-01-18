from channels.consumer import AsyncConsumer
from .models import Game, GameMatrix
from channels.db import database_sync_to_async
from .helper import *
from channels.exceptions import StopConsumer
import json

class GameConsumer(AsyncConsumer):
    async def websocket_connect(self, event):

        self.game_code = self.scope['url_route']['kwargs']['game_code']
        self.game_matrix_id = self.scope['url_route']['kwargs']['game_matrix_id']
        self.player_name = self.scope['url_route']['kwargs']['player_name']
        self.player_type = self.scope['url_route']['kwargs']['player_type']

        game_object = await database_sync_to_async(Game.objects.filter)(game_code=self.game_code)
        game_exists = await database_sync_to_async(game_object.exists)()
        player_object = await database_sync_to_async(Game.objects.filter)(game_code=self.game_code, game_opponent='to-be-decided')
        player_exists = await database_sync_to_async(player_object.exists)()

        if(not game_exists or player_exists):
            await self.channel_layer.group_add(self.game_code, self.channel_name)

        self.game_id = await setup_game(self.game_code, self.game_matrix_id, self.player_name, self.player_type)
        
        await self.send({
            'type':'websocket.accept',
        })

    async def websocket_receive(self, event):

        await update_matrix(self.game_matrix_id, event['text'], self.player_type)
        self.result = await check_winner(self.game_matrix_id)

        if(self.result == 44):
            await self.channel_layer.group_send(self.game_code, {
                'type': 'send.message',
                'message':json.dumps({"msg_type":"result", "msg":self.player_name})
            })
        elif(self.result == 11):
            await self.channel_layer.group_send(self.game_code, {
                'type': 'send.message',
                'message':json.dumps({"msg_type":"result", "msg":self.player_name})
            })
        elif(self.result == False):
            await self.channel_layer.group_send(self.game_code, {
                'type': 'send.message',
                'message':json.dumps({"msg_type":"result", "msg":"game drawn"})
            })
        await self.channel_layer.group_send(self.game_code, {
                'type': 'send.message',
                'message': json.dumps({"msg_type":"chance", "position":event['text'], "symbol":self.player_type})
            })

    async def send_message(self, event):
        await self.send({
            'type':'websocket.send',
            'text':event['message']
        })

    async def websocket_disconnect(self, event):
        
        game_matrix = await database_sync_to_async(GameMatrix.objects.get)(id=self.game_matrix_id)
        await database_sync_to_async(game_matrix.delete)()
        raise StopConsumer()