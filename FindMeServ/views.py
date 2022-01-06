import traceback

from django.shortcuts import render
from FindMeServ.models import Server
import a2s
import logging

logger = logging.getLogger('FindMeServ views')


def home(request):
    return render(request, '../templates/base.html')


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
        add_server_statement = (True, 'The server has been added to the database')
    except Exception:
        logging.error(traceback.format_exc())
        add_server_statement = (False, 'Impossible to add the server')

    logger.error(type(add_server_statement))
    context = {'types': Server.ServerType.choices, 'add_server_statement': add_server_statement}
    return render(request, '../templates/addServer.html', context)


def server_list(request):
    empty = request.POST.get('empty')
    host = request.POST.get('host')
    gamemode = request.POST.get('gamemode')

    servers = Server.objects.all()

    logger.error(host)
    if host != "":
        servers = servers.filter(host=host)

    logger.error(gamemode)
    if gamemode != "None":
        servers = servers.filter(gamemode=gamemode)

    servers_to_send = []
    for server in servers:
        info = get_server_info(server)
        if (info.player_count != 0 and empty is None) or empty == 'on':
            servers_to_send.append({
                'ip': server.get_ip(),
                'port': server.get_port(),
                'map': info.map_name,
                'player': info.player_count,
                'max_player': info.max_players,
                'gamemode': server.get_gamemode_display(),
                'host': server.get_host(),
                'name': info.server_name,
            })

    logger.error(servers_to_send)
    context = {'servers': servers_to_send, 'types': Server.ServerType.choices, 'empty': empty, 'host': host,
               'gamemode': gamemode}
    return render(request, '../templates/serverList.html', context)


# TODO parallel
def get_server_info(server):
    address = (server.get_ip(), server.get_port())
    return a2s.info(address)
