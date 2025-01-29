import sys
import requests
from translate import Translator

from config.settings import KZT_RATE


class SteamService:
    @staticmethod
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
            return {'response':True, 'data':data.get('response', {}).get('steamid')}
        else:
            print(response.__dict__, file=sys.stderr)
            return {'response':False, 'data': f'{response.status_code}: {response.reason}'}

    @staticmethod
    def get_game_info(appid):
        """Возвращает информацию об игре"""
        url = f'http://store.steampowered.com/api/appdetails?appids={appid}&cc=kz'
        response = requests.get(url)
        game_object = None
        if response.status_code == 200:
            response_data = response.json()
            if response_data[str(appid)]['success']:
                game_object = response_data[str(appid)]['data']
                # цена
                if "price_overview" in game_object:
                    if game_object["price_overview"]['currency'] == 'KZT':
                        game_object['price'] = str(int(KZT_RATE * float(game_object["price_overview"]['final']) / 100)) + " РУБ (KZ)"
                    else:
                        game_object['price'] = game_object["price_overview"]['final_formatted']
                # перевод
                translator = Translator(to_lang="ru")
                game_object['short_description'] = translator.translate(game_object['short_description'])
        return game_object

    @staticmethod
    def get_steam_games_list(userid, apikey):
        """Возвращает список игр пользователя"""
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
                    # время
                    time = round(game['playtime_forever'] / 60, 1)
                    if int(time) == time:
                        time = int(time)

                    games_list.append({
                        'title': game['name'],
                        'appid': game['appid'],
                        'time': time,
                    })
                sorted_games_list = sorted(games_list, key=lambda x: x.get('time', 0), reverse=True)
                return sorted_games_list
            else:
                return None
        else:
            print(f"Ошибка: {response.status_code}", file=sys.stderr)
            return None

