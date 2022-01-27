import a2s
import logging
import re
from django.http import JsonResponse
from enum import Enum

logger = logging.getLogger('server utils')


def get_server_info(server):
    address = (server.get_ip(), server.get_port())
    try:
        return a2s.info(address, timeout=0.5)
    except Exception as e:
        logger.error("Server " + str(server.get_id()) + " (" + str(server.get_ip()) + ":" + str(
            server.get_port()) + ") timed out")
        return None


def get_players_info(request):
    ip = request.POST.get('ip')
    port = request.POST.get('port')

    try:
        address = (ip, int(port))
        players = a2s.players(address)
    except Exception:
        return JsonResponse({'players': None})

    players_array = []
    for player in players:
        players_array.append({
            'name': player.name,
            'score': player.score,
            'duration': int(player.duration)
        })

    return JsonResponse({'players': players_array})


def extract_server_info(server, empty, maps, result, index):
    info = get_server_info(server)

    if (info is None) or \
            (int(info.player_count) == 0 and empty == 'None') or \
            ('all' not in maps and info.map_name not in maps):
        result[index] = None
        return

    server_rank_re = re.search(r'#[0-9]+', info.server_name)

    try:
        server_rank = int(server_rank_re.group(0).replace('#', ''))
    except Exception:
        server_rank = 0

    result[index] = {
        'ip': server.get_ip(),
        'port': server.get_port(),
        'map': info.map_name,
        'player': info.player_count + info.bot_count,
        'max_player': info.max_players,
        'gamemode': server.get_gamemode_display(),
        'host': server.get_host(),
        'name': info.server_name,
        'server_rank': server_rank,
    }


class Map(Enum):
    all = 0
    de_ancient = 1
    de_cache = 2
    de_dust2 = 3
    de_inferno = 4
    de_mirage = 5
    de_nuke = 6
    de_overpass = 7
    de_train = 8
    de_vertigo = 9
