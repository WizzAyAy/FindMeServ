import traceback

from FindMeServ.models import Server
from django.shortcuts import render

from .serverUtils import *


def add_server_form(request):
    types = Server.ServerType.choices
    context = {'types': types}
    return render(request, '../templates/servers/addServer.html', context)


def add_server(request):
    ip = request.POST.get('ip')
    port = request.POST.get('port')
    host = request.POST.get('host')
    gamemode = request.POST.get('gamemode')

    try:
        server = Server.objects.create(
            ip=ip,
            port=port,
            host=host,
            gamemode=gamemode
        )
        if get_server_info(server) is None:
            server.delete()
            raise Exception("server cannot be reached")
        add_server_statement = (True, 'The server has been added to the database')
    except Exception:
        logging.error(traceback.format_exc())
        add_server_statement = (False, 'Impossible to add the server')

    context = {'types': Server.ServerType.choices, 'add_server_statement': add_server_statement}
    return render(request, '../templates/servers/addServer.html', context)
