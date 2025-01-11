from django.shortcuts import get_object_or_404
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

        object = SteamService.get_game_info(game_id)
        if object:
            context['object'] = object
            context['developers'] = ','.join(object['developers'])
            context['publishers'] = ','.join(object['publishers'])
        else:
            details = steam.apps.get_app_details(game_id)
            context['object'] = details[game_id]['data'] if details[game_id]['success'] else None

        return context


class GameDetailView(DetailView):
    """Страница игры"""

    model = Game
    template_name = 'detail.html'
    is_full_data = False

    def get_object(self, queryset=None, **kwargs):
        self.object = self.model.objects.filter(pk=(self.kwargs['pk'])).first()

        # получение объекта из Steam API
        if self.object:
            # если есть объект в БД
            self.is_full_data = True
        else:
            steam = Steam(STEAM_API_KEY)
            game_id = self.kwargs.get('pk')
            self.object = SteamService.get_game_info(game_id)
            if self.object:
                # если получена полная информация об объекте из API
                self.is_full_data = True
            else:
                details = steam.apps.get_app_details(game_id)
                if details:
                    self.object = details[str(game_id)]['data']

        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.is_full_data:
            context['developers'] = ','.join(self.object['developers'])
            context['publishers'] = ','.join(self.object['publishers'])
            self.is_full_data = False

        return context
