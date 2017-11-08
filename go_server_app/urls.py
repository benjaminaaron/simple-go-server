from django.conf.urls import url

from . import views

app_name = 'go_server_app'  # namespacing
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^game/(?P<game_id>[a-zA-Z0-9]+)$', views.game, name='game'),
    url(r'^terminal/$', views.terminal, name='terminal'),
]
