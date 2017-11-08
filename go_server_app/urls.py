from django.conf.urls import url

from . import views

app_name = 'go_server_app'  # namespacing
urlpatterns = [
    url(r'^$', views.index, name='index'),
]
