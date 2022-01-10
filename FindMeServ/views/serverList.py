from FindMeServ.models import Server
from threading import Thread
from django.shortcuts import render

from .serverUtils import *
import logging

logger = logging.getLogger('serverList')


def server_list(request):
    empty = request.POST.get('empty', 'None')
    host = request.POST.get('host', '')
    gamemode = request.POST.get('gamemode', 'None')
    maps = get_map_list(request)

    servers = Server.objects.all()

    if host != '':
        servers = servers.filter(host=host)

    if gamemode != 'None':
        servers = servers.filter(gamemode=gamemode)

    servers_to_send = []

    threads = [None] * servers.count()
    infos = [None] * servers.count()

    index = 0

    for server in servers:
        threads[index] = Thread(target=extract_server_info, args=(server, empty, maps, infos, index))
        threads[index].start()
        index += 1

    for i in range(len(threads)):
        threads[i].join()

    for info in infos:
        if info is not None:
            servers_to_send.append(info)

    servers_to_send = sorted(servers_to_send, key=lambda d: d['server_rank'])

    context = {'servers': servers_to_send, 'types': Server.ServerType.choices, 'empty': empty, 'host': host,
               'gamemode': gamemode, 'maps': Map.__members__, 'maps_checked': maps}
    return render(request, '../templates/serverList.html', context)


def get_map_list(request):
    maps = []
    for map_ in Map.__members__:
        if map_ == 'all':
            get_map = request.POST.get(map_, 'on')
        else:
            get_map = request.POST.get(map_)

        if get_map == 'on':
            maps.append(map_)
    return maps
