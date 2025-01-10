from django.views.generic import TemplateView
from steam_web_api import Steam

from config.settings import STEAM_API_KEY
from main.services import get_steam_games_list, get_game_info, get_steam_userid

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
