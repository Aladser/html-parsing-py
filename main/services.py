import sys
import requests

def get_steam_userid(login, api_key):
    """Возвращает ID пользователя стим"""
    url = f'https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/'
    params = {
        'key': api_key,
        'vanityurl': login
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get('response', {}).get('steamid')
    else:
        print(f'Ошибка: {response.status_code}', file=sys.stderr)
        return None

def get_game_info(appid):
    """Возвращает информацию об игре"""
    url = f'https://store.steampowered.com/api/appdetails?appids={appid}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data[str(appid)]['success']:
            gameinfo = data[str(appid)]['data']
            # 'metacritic': gameinfo['metacritic'] if 'metacritic' in gameinfo else '',
            return {
                'type':gameinfo['type'],
                'name': gameinfo['name'],
                'short_description': gameinfo['short_description'],
                'image': gameinfo['capsule_image'],
                'background': gameinfo['background'],
                'release_date': gameinfo['release_date']['date'],
                'developers': ', '.join(gameinfo['developers']),
                'publishers': ', '.join(gameinfo['publishers']),
                'genres': ', '.join([genre['description'] for genre in gameinfo['genres']]),
                'categories': ', '.join([genre['description'] for genre in gameinfo['categories']]),
            }
        else:
            return None
    else:
        print(f'Ошибка: {response.status_code}', file=sys.stderr)
        return None

def get_steam_games_list(userid, apikey):
    url = f'https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/'
    params = {
        'key': apikey,
        'steamid': userid,
        'include_appinfo': True,
        'include_played_free_games': True,
        'format': 'json'
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        games_data = response.json()
        owned_games = games_data.get('response', {}).get('games', [])
        games_list = []

        if owned_games:
            for game in owned_games:
                games_list.append({
                    'title': game['name'],
                    'appid': game['appid'],
                    'time': round(game['playtime_forever']/60, 2),
                })
            sorted_games_list = sorted(games_list, key=lambda x: x.get('time', 0), reverse=True)
            return sorted_games_list
        else:
            return None
    else:
        print(f"Ошибка: {response.status_code}", file=sys.stderr)
        return None
