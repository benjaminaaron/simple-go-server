from django.shortcuts import render

from .models import GameMeta


def index(request):
    return render(request, 'go_server_app/index.html')


def dashboard(request):
    return render(request, 'go_server_app/dashboard.html', {'games_list': GameMeta.objects.all()})


def game(request, game_id):
    game_meta = GameMeta.objects.get(game_id=game_id)
    return render(request, 'go_server_app/game.html', {'game_meta': game_meta})
