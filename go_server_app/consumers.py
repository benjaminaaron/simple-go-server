import json

from channels.sessions import channel_session

from . import GamesManager
from .models import GameStatus, GameMeta
from .utils import to_text_dict, normalize_color_string


@channel_session
def ws_connect(message):
    channel = message.reply_channel
    channel.send({"accept": True})
    channel.send(to_text_dict("Welcome to the Go Server. Use \"list_games\", "
                              "\"create_game\" or \"join_game <game_id> <username> <color>\""))


@channel_session
def ws_message(message):
    command = message.content['text'].strip()  # strip() is same as trim() in Java, removes whitespaces at start and end
    channel = message.reply_channel

    game_play = GamesManager.get_game_associated_with_channel_name(channel.name)
    if game_play is not None:
        game_play.handle_command(channel.name, command)
        return

    # if channel.name not yet known -> in meta mode
    if command == 'list_games':
        games_json_arr = []
        for game_meta in GameMeta.objects.all():
            games_json_arr.append(game_meta.serialize_to_json())
        channel.send(to_text_dict(json.dumps(games_json_arr)))
        return

    if command.startswith('create_game'):  # support parameters: board_size, komi, time_settings, what else? TODO
        game_meta = GameMeta.objects.create_game()
        channel.send(to_text_dict("Created game with ID " + game_meta.game_id))
        return

    if command.startswith('join_game'):
        params = command.split(' ')[1:]
        if len(params) != 3:
            channel.send(to_text_dict("join_game requires three arguments: \"join_game <game_id> <username> <color>\""))
            return

        game_id = params[0]
        username = params[1]
        color = normalize_color_string(params[2])

        if not GameMeta.objects.filter(game_id=game_id).exists():
            channel.send(to_text_dict("There is no game with the ID " + game_id))
            return

        # this game exists
        game_meta = GameMeta.objects.get(game_id=game_id)

        if game_meta.status != GameStatus.WAITING_FOR_PLAYERS:
            channel.send(to_text_dict("This game is not waiting for players."))
            return

        if not game_meta.color_available(color):
            channel.send(to_text_dict("This color is already taken."))
            return

        if not game_meta.username_available(username):
            channel.send(to_text_dict("The other player has the same username."))
            return

        # if you reach here, you can join this game
        GamesManager.assign_player_to_game(game_meta, channel.name, username, color)


@channel_session
def ws_disconnect(message):
    print(message)
