from django.contrib import admin

from .models import GameMeta


class GameMetaAdmin(admin.ModelAdmin):
    list_display = ('game_id', 'status', 'creation_date')
    # list_filter = ['creation_date']


admin.site.register(GameMeta, GameMetaAdmin)
