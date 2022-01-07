import traceback
from types import NoneType

from django.http import JsonResponse
from django.shortcuts import render
from FindMeServ.models import Server
import a2s
import logging
import re
from threading import Thread

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

    context = {'types': Server.ServerType.choices, 'add_server_statement': add_server_statement}
    return render(request, '../templates/addServer.html', context)


def server_list(request):
    empty = request.POST.get('empty', 'None')
    host = request.POST.get('host', '')
    gamemode = request.POST.get('gamemode', 'None')

    servers = Server.objects.all()

    if host != "":
        servers = servers.filter(host=host)

    if gamemode != "None":
        servers = servers.filter(gamemode=gamemode)

    servers_to_send = []

    threads = [None] * servers.count()
    infos = [None] * servers.count()

    index = 0

    for server in servers:
        threads[index] = Thread(target=extract_server_info, args=(server, empty, infos, index))
        threads[index].start()
        index += 1

    for i in range(len(threads)):
        threads[i].join()

    for info in infos:
        if info is not None:
            servers_to_send.append(info)

    servers_to_send = sorted(servers_to_send, key=lambda d: d['server_rank'])

    context = {'servers': servers_to_send, 'types': Server.ServerType.choices, 'empty': empty, 'host': host,
               'gamemode': gamemode}
    return render(request, '../templates/serverList.html', context)


def get_server_info(server):
    address = (server.get_ip(), server.get_port())
    try:
        return a2s.info(address, timeout=0.2)
    except Exception:
        return None


def get_players_info(request):
    address = request.POST.get('ip') + ':' + request.POST.get('port')
    logger.error(address)
    try:
        players = a2s.players(address)
    except Exception:
        players = None
    return JsonResponse({"players": players})


def extract_server_info(server, empty, result, index):
    info = get_server_info(server)

    if (info is None) or (int(info.player_count) == 0 and empty is "None"):
        result[index] = None
        return

    server_rank_re = re.search(r"#[0-9]+", info.server_name)
    server_rank = 0
    if type(server_rank_re) != NoneType:
        server_rank = int(server_rank_re.group(0).replace('#', ''))
    result[index] = {
        'ip': server.get_ip(),
        'port': server.get_port(),
        'map': info.map_name,
        'player': info.player_count,
        'max_player': info.max_players,
        'gamemode': server.get_gamemode_display(),
        'host': server.get_host(),
        'name': info.server_name,
        'server_rank': server_rank,
    }
