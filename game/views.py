from django.views.generic import DetailView, TemplateView
from django.views.generic import ListView
from steam_web_api import Steam
from config.settings import STEAM_API_KEY
from game.models import Game
from libs.steam_service import SteamService


class GameListView(ListView):
    """Список игр"""
    model = Game
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        login = self.request.GET['login'] if 'login' in self.request.GET else None
        userid = SteamService.get_steam_userid(login, STEAM_API_KEY)
        games_list = SteamService.get_steam_games_list(userid, STEAM_API_KEY) if login else None
        context['games'] = games_list
        context['login'] = login
        context['userid'] = userid
        return context


class GameView(TemplateView):
    """Страница игры"""

    template_name = 'detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        steam = Steam(STEAM_API_KEY)
        game_id = kwargs.get('id')

        info = SteamService.get_game_info(game_id)
        if info:
            context['info'] = info
            context['developers'] = ','.join(info['developers'])
            context['publishers'] = ','.join(info['publishers'])
        else:
            details = steam.apps.get_app_details(game_id)
            context['info'] = details[game_id]['data'] if details[game_id]['success'] else None

        return context


class GameDetailView(DetailView):
    model = Game
    template_name = 'detail.html'

