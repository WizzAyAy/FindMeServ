import requests
from django.http import JsonResponse
from django.shortcuts import render
from threading import Thread

import environ


def get_room(request):
    return render(request, '../templates/faceit/match_room.html')


def get_room_stats(request):

    env = environ.Env()
    environ.Env.read_env()

    room_id = request.POST.get('room_id')
    token = env('FACEIT_TOKEN')

    match_details = retrieve_room_details(room_id, token)

    faction_1 = match_details.json()['teams']['faction1']
    faction_2 = match_details.json()['teams']['faction2']

    stats_teams_1 = retrieve_faction_stats(faction_1, token)
    stats_teams_2 = retrieve_faction_stats(faction_2, token)

    return JsonResponse({
        'id': room_id,
        'stats_team_1': stats_teams_1,
        'stats_team_2': stats_teams_2,
    })


def retrieve_room_details(room_id, token):
    url = 'https://open.faceit.com/data/v4/matches/' + room_id

    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + token,
    }

    return requests.get(url, headers=headers)


def retrieve_faction_stats(faction, token):
    players = faction['roster']
    name = faction['name']

    threads = [None] * 5
    players_stats = [None] * 5

    index = 0

    for player in players:
        threads[index] = Thread(target=retrieve_player_stats, args=(player, token, players_stats, index))
        threads[index].start()
        index += 1

    for i in range(len(threads)):
        threads[i].join()

    return {'team_name': name, 'team_info': collapse_player_stats(players_stats)}


def collapse_player_stats(players_stats):
    maps_stats = {}
    teams_stats = {'game_skill_level': 0}
    nicknames = []

    for player_stats in players_stats:
        game_skill_level = int(player_stats['game_skill_level'])
        teams_stats['game_skill_level'] += game_skill_level
        game_skill_level_all = int(teams_stats['game_skill_level'])

        nicknames.append(player_stats['nickname'])

        for csgo_map in sorted(player_stats['maps']):
            try:
                win_rate_all = int(maps_stats[csgo_map]['Win Rate %'])
                win_rate = int(player_stats['maps'][csgo_map]['Win Rate %'])

                maps_stats[csgo_map]['times_played'] += int(player_stats['maps'][csgo_map]['times_played'])
                maps_stats[csgo_map]['Win Rate %'] = int(
                    ((win_rate_all * game_skill_level_all) + (win_rate * game_skill_level)) /
                    (game_skill_level_all + game_skill_level)
                )

            except Exception:
                maps_stats[csgo_map] = {}
                maps_stats[csgo_map]['times_played'] = int(player_stats['maps'][csgo_map]['times_played'])
                maps_stats[csgo_map]['Win Rate %'] = int(player_stats['maps'][csgo_map]['Win Rate %'])
                maps_stats[csgo_map]['img'] = player_stats['maps'][csgo_map]['img']

    return {'teams_stats': teams_stats, 'maps_stats': maps_stats, 'nicknames': nicknames}


def retrieve_player_stats(player, token, players_stats, index):
    url = 'https://open.faceit.com/data/v4/players/' + player['player_id'] + '/stats/csgo'

    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + token,
    }

    player_stats = requests.get(url, headers=headers)

    stats = {
        'nickname': player['nickname'],
        'game_skill_level': int(player['game_skill_level']),
        'lifetime_matches': int(player_stats.json()['lifetime']['Matches']),
        'maps': {}
    }

    for segment in player_stats.json()['segments']:
        if segment['mode'] == '5v5':
            csgo_map = segment['label']

            stats['maps'][csgo_map] = {}
            stats['maps'][csgo_map]['Win Rate %'] = int(segment['stats']['Win Rate %'])
            stats['maps'][csgo_map]['times_played'] = int(segment['stats']['Matches'])
            stats['maps'][csgo_map]['img'] = segment['img_regular']

    players_stats[index] = stats
