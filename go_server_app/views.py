from django.shortcuts import render


def index(request):
    return render(request, 'go_server_app/index.html')
