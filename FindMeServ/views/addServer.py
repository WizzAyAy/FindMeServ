import traceback

from FindMeServ.models import Server
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .serverUtils import *


@login_required
def add_server(request):
    if request.method == 'GET':
        types = Server.ServerType.choices
        context = {'types': types}
        return render(request, '../templates/servers/addServer.html', context)

    if request.method == 'POST':
        ip = request.POST.get('ip')
        port = request.POST.get('port')
        host = request.POST.get('host')
        gamemode = request.POST.get('gamemode')

        try:
            server = Server.objects.create(
                ip=ip,
                port=port,
                host=host,
                gamemode=gamemode,
                owner=request.user
            )
            if get_server_info(server) is None:
                server.delete()
                raise Exception("server cannot be reached")
            add_server_statement = (True, 'The server has been added to the database')
        except Exception:
            logging.error(traceback.format_exc())
            add_server_statement = (False, 'Impossible to add this server')

        context = {'types': Server.ServerType.choices, 'add_server_statement': add_server_statement}
        return render(request, '../templates/servers/addServer.html', context)
