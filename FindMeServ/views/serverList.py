from django.contrib.auth import get_user_model

from FindMeServ.models import Server
from threading import Thread
from django.shortcuts import render

from .serverUtils import *
import logging

logger = logging.getLogger('serverList')


def server_list(request):
    empty = request.POST.get('empty', 'None')
    owned = request.POST.get('owned', 'None')
    host = request.POST.get('host', '')
    gamemode = request.POST.get('gamemode', 'None')
    maps = get_map_list(request)

    user_model = get_user_model()
    users_admin = user_model.objects.all().filter(is_staff=True)
    servers = Server.objects.all().filter(owner__in=users_admin)

    if owned != 'None' and request.user.is_authenticated:
        servers = servers.filter(owner=request.user)

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

    context = {
        'servers': servers_to_send,
        'types': Server.ServerType.choices,
        'empty': empty,
        'owned': owned,
        'host': host,
        'gamemode': gamemode,
        'maps': Map.__members__,
        'maps_checked': maps
    }
    return render(request, '../templates/servers/serverList.html', context)


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
