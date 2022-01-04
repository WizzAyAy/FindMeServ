import traceback

from django.shortcuts import render
from FindMeServ.models import Server
import a2s
import logging

logger = logging.getLogger('FindMeServ views')


def add_server_form(request):
    types = Server.ServerType.choices
    context = {'types': types}
    return render(request, '../templates/addServer.html', context)


def add_server(request):
    ip = request.POST.get('ip')
    port = request.POST.get('port')
    host = request.POST.get('host')
    gamemode = request.POST.get('gamemode')

    logger.error(ip)
    logger.error(port)
    logger.error(host)
    logger.error(gamemode)


    try:
        Server.objects.create(
            ip=ip,
            port=port,
            host=host,
            gamemode=gamemode
        )
        add_server_statement = (True, "The server has been added to the database")
    except Exception:
        logging.error(traceback.format_exc())
        add_server_statement = (False, "Impossible to add the server")

    types = Server.ServerType.choices

    logger.error(type(add_server_statement))
    context = {'types': types, 'add_server_statement': add_server_statement}
    return render(request, '../templates/addServer.html', context)


def test(request):
    address = ("145.239.5.44", 27015)
    info = a2s.info(address)
    players = a2s.players(address)
    context = {'info': info, 'players': players}
    return render(request, '../templates/hello.html', context)
