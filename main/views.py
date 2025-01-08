from django.views.generic import TemplateView
from steam_web_api import Steam
from config.settings import STEAM_USER_ID, STEAM_API_KEY
from main.services import get_steam_games_list, get_game_info, get_steam_userid


class MainView(TemplateView):
    """Главная страница"""

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

    template_name = 'game.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        steam = Steam(STEAM_API_KEY)

        request_list = self.request.path.split('/')
        gameid = request_list[-1]

        info = get_game_info(gameid)
        if info:
            context['info'] = info
            context['developers'] = ','.join(info['developers'])
            context['publishers'] = ','.join(info['publishers'])
        else:
            details = steam.apps.get_app_details(gameid)
            context['info'] = details[gameid]['data'] if details[gameid]['success'] else None
            """
            for k,v in details[gameid]['data'].items():
                print(f"{k} - {v}")
            """

        return context
