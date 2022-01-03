from django.shortcuts import render
from FindMeServ.models import Server
import a2s
import logging

logger = logging.getLogger('FindMeServ views')


def add_server(request):
    types = Server.ServerType.choices
    context = {'types': types}
    return render(request, '../templates/addServer.html', context)


def test(request):
    address = ("145.239.5.44", 27015)
    info = a2s.info(address)
    players = a2s.players(address)
    # rules = a2s.rules(address)
    context = {'info': info, 'players': players}
    return render(request, '../templates/hello.html', context)
