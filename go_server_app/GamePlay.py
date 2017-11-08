from .models import GameMeta
from .utils import to_text_dict
from channels import Channel


class GamePlay:
    def __init__(self, game_id):
        self.game_id = game_id
        self.current_player = None
        self.black_player_channel_name = None
        self.white_player_channel_name = None
        # add spectator channels TODO

    def start(self):
        game_meta = GameMeta.objects.get(game_id=self.game_id)
        message = 'Game started with black player ' + game_meta.black_player \
                  + ' and white player ' + game_meta.white_player
        if self.black_player_channel_name == self.white_player_channel_name:
            message += ' (both you)'  # two players one the same channel
        self.broadcast(message)
        self.broadcast('Now switching to Go Text Protocol')

    def broadcast(self, message):
        Channel(self.black_player_channel_name).send(to_text_dict(message))
        # if two players come from same channel, send message only once
        if self.black_player_channel_name != self.white_player_channel_name:
            Channel(self.white_player_channel_name).send(to_text_dict(message))

    def handle_command(self, channel_name, command):
        print('got command ' + command + ' from channel ' + channel_name)

        # TODO
