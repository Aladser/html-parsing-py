import requests
from django.views.generic import TemplateView

from config.settings import STEAM_USER_ID, STEAM_API_KEY
from main.services import get_steam_games_list

page = '/site/index.html'

class MainView(TemplateView):
    """Представление главной страницы"""

    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        games_list = get_steam_games_list(STEAM_USER_ID, STEAM_API_KEY)
        context['games'] = games_list

        return context
