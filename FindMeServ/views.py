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
        add_server_statement = (True, 'The server has been added to the database')
    except Exception:
        logging.error(traceback.format_exc())
        add_server_statement = (False, 'Impossible to add the server')

    types = Server.ServerType.choices

    logger.error(type(add_server_statement))
    context = {'types': types, 'add_server_statement': add_server_statement}
    return render(request, '../templates/addServer.html', context)



def server_list(request):
    servers = Server.objects.all()
    servers_to_send = []
    for server in servers:
        info = get_server_info(server)
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
    context = {'servers': servers_to_send}
    return render(request, '../templates/serverList.html', context)


# TODO parallel
def get_server_info(server):
    address = (server.get_ip(), server.get_port())
    return a2s.info(address)
