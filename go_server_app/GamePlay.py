from .models import GameMeta
from .utils import to_text_dict
from channels import Channel


def send(channel_name, message):
    Channel(channel_name).send(to_text_dict(message))


class GamePlay:
    def __init__(self, game_id):
        self.game_id = game_id
        # the three following are channel names as strings, not usernames or IDs
        self.current_player = None
        self.black_player = None
        self.white_player = None
        # add spectator channels TODO

    def start(self):
        game_meta = GameMeta.objects.get(game_id=self.game_id)
        message = 'Game started with black player ' + game_meta.black_player \
                  + ' and white player ' + game_meta.white_player
        if self.black_player == self.white_player:
            message += ' (both you)'  # two players one the same channel
        self.broadcast(message)
        self.broadcast('Now switching to Go Text Protocol')
        self.next_turn()

    def next_turn(self):
        if self.current_player is None:
            self.current_player = self.black_player
        elif self.current_player == self.black_player:
            self.current_player = self.white_player
        else:
            self.current_player = self.black_player
        send(self.current_player, 'genmove ' + self.get_color_of_current_player())

    def broadcast(self, message):
        send(self.black_player, message)
        # if two players come from same channel, send message only once
        if self.black_player != self.white_player:
            send(self.white_player, message)

    def get_color_of_current_player(self):
        if self.current_player == self.black_player:
            return 'b'
        return 'w'

    def is_color_of_current_player(self, col):
        if col == 'white':
            col = 'w'
        if col == 'black':
            col = 'b'
        return col == self.get_color_of_current_player()

    def get_other_player(self):
        if self.current_player == self.black_player:
            return self.white_player
        return self.black_player

    def handle_command(self, channel_name, command):
        print('got command ' + command + ' from channel ' + channel_name)

        if command == 'showboard':
            send(channel_name, '')
            return

        if command.startswith('play'):
            if channel_name != self.current_player:
                send(channel_name, '? not your turn')
                return
            args = command.split(' ')[1:]

            if len(args) != 2:
                send(self.current_player, '? two arguments required, your color and your move')
                return
            col = args[0]
            if not self.is_color_of_current_player(col):
                send(self.current_player, '? your color is not ' + col)
                return
            move = args[1]

            # TODO place stone on own engine to validate coordinates and legality of move

            send(self.current_player, '= stone placed at ' + move)
            send(self.get_other_player(), 'play ' + col + ' ' + move)
            self.next_turn()
            return

        if command == '':
            send(channel_name, '')
            return

        if command == '':
            send(channel_name, '')
            return


# lysator.liu.se/~gunnar/gtp/gtp2-spec-draft2/gtp2-spec.html#SECTION00070000000000000000
# All implementations are required to support the following commands:
# protocol_version  [ ]
# name              [ ]
# version           [ ]
# known_command     [ ]
# list_commands     [ ]
# quit              [ ]
# boardsize         [ ]
# clear_board       [ ]
# komi              [ ]
# play              [x]
# genmove           [ ]
