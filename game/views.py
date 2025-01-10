from django.views.generic import DetailView, TemplateView
from django.views.generic import ListView
from steam_web_api import Steam
from config.settings import STEAM_API_KEY
from game.models import Game
from main.services import get_steam_userid, get_steam_games_list, get_game_info


class GameListView(ListView):
    model = Game
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        login = self.request.GET['login'] if 'login' in self.request.GET else None
        userid = get_steam_userid(login, STEAM_API_KEY)
        games_list = get_steam_games_list(userid, STEAM_API_KEY) if login else None
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

        gameid = kwargs.get('id')
        info = get_game_info(gameid)
        if info:
            context['info'] = info
            context['developers'] = ','.join(info['developers'])
            context['publishers'] = ','.join(info['publishers'])
        else:
            details = steam.apps.get_app_details(gameid)
            context['info'] = details[gameid]['data'] if details[gameid]['success'] else None

        return context


class GameDetailView(DetailView):
    model = Game
    template_name = 'detail.html'

