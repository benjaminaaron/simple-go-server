from django.db import models
from datetime import datetime
from enumfields import Enum, EnumField

from .utils import gen_random_string


class GameStatus(Enum):
    WAITING_FOR_PLAYERS = 0
    ONGOING = 1
    ENDED = 2


class GameMetaManager(models.Manager):
    def create_game(self):
        game_meta = self.create(game_id=gen_random_string(8, lower_case=False))
        return game_meta


class GameMeta(models.Model):
    game_id = models.CharField(max_length=30, default='n/a')
    status = EnumField(GameStatus, default=GameStatus.WAITING_FOR_PLAYERS)
    creation_date = models.DateTimeField(default=datetime.now)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    board_size = models.IntegerField(default=9)
    history = models.TextField(blank=True, null=True)
    black_player = models.CharField(max_length=30, default='n/a')
    white_player = models.CharField(max_length=30, default='n/a')

    def serialize_to_json(self):
        return {
            'game_id': self.game_id,
            'status': self.status.label,
            # 'creation_date': self.creation_date.isoformat(),
            # 'board_size': self.board_size,
            # 'history': self.history,
            # 'black_player': self.black_player,
            # 'white_player': self.white_player,
        }

    def color_available(self, color):
        if color == 'w':
            if self.white_player != 'n/a':
                return False
        if color == 'b':
            if self.black_player != 'n/a':
                return False
        return True

    def username_available(self, username):
        return self.white_player != username and self.black_player != username

    def set_black_player(self, username):
        self.black_player = username
        self.save()

    def set_white_player(self, username):
        self.white_player = username
        self.save()

    objects = GameMetaManager()
