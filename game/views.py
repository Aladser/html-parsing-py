import sys
from math import floor

from django.views.generic import DetailView
from django.views.generic import ListView

from config.settings import STEAM_API_KEY
from game.models import Game
from libs.game_service import GameService
from libs.steam_service import SteamService


class GameListView(ListView):
    model = Game
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        login = context['login'] = self.request.GET['login'] if 'login' in self.request.GET else None
        if login:
            user_request = SteamService.get_steam_userid(login, STEAM_API_KEY)
            if user_request['response']:
                userid = user_request['data']
                games_list = SteamService.get_steam_games_list(userid, STEAM_API_KEY)
                context['games'] = games_list
                context['userid'] = userid

                context['games_count'] = len(games_list)
                total_time = sum([game['time'] for game in games_list])
                context['avg_time'] = round(total_time / context['games_count'], 2)

                game_time_stat = {
                    '250 часов': {'count': 0, 'percent': 0},
                    '100 часов': {'count': 0, 'percent': 0},
                    '50 часов': {'count': 0, 'percent': 0},
                    '20 часов': {'count': 0, 'percent': 0},
                    '12 часов': {'count': 0, 'percent': 0},
                    'менее 12 часов': {'count': 0, 'percent': 0},
                    '0 часов': {'count': 0, 'percent': 0}
                }
                for game in games_list:
                    if game['time'] >= 250:
                        game_time_stat['250 часов']['count'] += 1
                    if game['time'] >= 100:
                        game_time_stat['100 часов']['count'] += 1
                    if game['time'] >= 50:
                        game_time_stat['50 часов']['count'] += 1
                    if game['time'] >= 20:
                        game_time_stat['20 часов']['count'] += 1
                    if game['time'] >= 12:
                        game_time_stat['12 часов']['count'] += 1
                    elif game['time'] < 12 and game['time'] != 0:
                        game_time_stat['менее 12 часов']['count'] += 1
                    else:
                        game_time_stat['0 часов']['count'] += 1

                context['played_games_count'] = context['games_count'] - game_time_stat['0 часов']['count']
                for stat in game_time_stat:
                    game_time_stat[stat]['percent'] = round(
                        game_time_stat[stat]['count'] * 100 / context['played_games_count'])
                context['played_games_percent'] = floor(100 * context['played_games_count'] / context['games_count'])
                context['game_time_stat'] = game_time_stat

                return context
            else:
                context['error'] = user_request['data']
        context['games'] = None
        return context

class GameDetailView(DetailView):
    model = Game
    template_name = 'detail.html'

    def get_object(self, queryset=None, **kwargs):
        game_appid = self.kwargs.get('pk')
        self.object = self.model.objects.filter(pk=game_appid).first()

        if not self.object:
            # получение объекта из Steam API
            self.object = SteamService.get_game_info(game_appid)
            if self.object:
                self.object = GameService.insert_game(self.object)
            else:
                print(f'Ошибка получения данных', file=sys.stderr)

        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            obj_type = str(type(self.object))
            if obj_type == "<class 'dict'>":
                context["steam_appid"] = self.object["steam_appid"]
            elif obj_type == "<class 'game.models.Game'>":
                context["steam_appid"] = self.object.id
            context['developers'] = ','.join([dev.name for dev in self.object.developers.all()])
            context['publishers'] = ','.join([pub.name for pub in self.object.publishers.all()])

        return context
