# handles the mapping of GamePlay to GameMeta, manages ongoing games and who gets access to which etc.
from channels import Channel

from .models import GameStatus
from .utils import to_text_dict
from .GamePlay import GamePlay

GameID_to_GamePlay = {}
ChannelName_to_GamePlay = {}


def get_game_associated_with_channel_name(channel_name):
    if channel_name not in ChannelName_to_GamePlay:
        return None
    return ChannelName_to_GamePlay[channel_name]


def assign_player_to_game(game_meta, channel_name, username, color):
    game_id = game_meta.game_id
    if game_id not in GameID_to_GamePlay:
        GameID_to_GamePlay[game_id] = GamePlay(game_id)

    game_play = GameID_to_GamePlay[game_id]
    ChannelName_to_GamePlay[channel_name] = game_play

    if color == 'b':
        game_meta.set_black_player(username)
        game_play.black_player = channel_name
    if color == 'w':
        game_meta.set_white_player(username)
        game_play.white_player = channel_name

    ready_to_start = game_play.black_player is not None and game_play.white_player is not None

    if not ready_to_start:
        Channel(channel_name).send(to_text_dict('Waiting for a 2nd player to join...'))
        return

    game_meta.set_status(GameStatus.ONGOING)
    game_play.start()
