import sys

from django.views.generic import DetailView
from django.views.generic import ListView

from config.settings import STEAM_API_KEY
from game.models import Game, Developer, Publisher, Genre, Category
from libs.steam_service import SteamService


class GameListView(ListView):
    """Список игр"""

    model = Game
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        login = context['login'] = self.request.GET['login'] if 'login' in self.request.GET else None
        if login:
            userid = SteamService.get_steam_userid(login, STEAM_API_KEY)
            games_list = SteamService.get_steam_games_list(userid, STEAM_API_KEY)
            context['games'] = games_list
            context['userid'] = userid
        else:
            context['games'] =  None
        return context

"""
object.background
object.id
object.name
object.header_image
object.short_description
object.metacritic
    object.metacritic.url
    object.metacritic.score
object.release_date
object.genres
object.categories
"""
class GameDetailView(DetailView):
    """Страница игры"""

    model = Game
    template_name = 'detail.html'
    is_full_data = False

    def get_object(self, queryset=None, **kwargs):
        self.object = self.model.objects.filter(pk=(self.kwargs['pk'])).first()

        if self.object:
            self.is_full_data = True
        else:
            # получение объекта из Steam API
            game_id = self.kwargs.get('pk')
            games_data = SteamService.get_game_info(game_id)
            if games_data:
                self.object = games_data['data']
                self.is_full_data = games_data['is_full']

                if self.is_full_data:
                    print(self.object['steam_appid'])
                    print(self.object['name'])
                    print(self.object['short_description'])
                    print(self.object['metacritic'])
                    print(self.object['release_date'])
                    print(self.object['header_image'])
                    print(self.object['background'])

                    # Разработчики
                    for developer in self.object['developers']:
                        developer_obj = Developer.objects.filter(name=developer).first()
                        if not developer_obj:
                            developer_obj = Developer(name=developer)
                            developer_obj.save()

                    # Издатели
                    for publisher in self.object['publishers']:
                        publisher_obj = Publisher.objects.filter(name=developer).first()
                        if not publisher_obj:
                            publisher_obj = Publisher(name=publisher)
                            publisher_obj.save()

                    # Жанры
                    for genre in self.object['genres']:
                        genre_obj = Genre.objects.filter(name=genre['description']).first()
                        if not genre_obj:
                            genre_obj = Genre(name=genre['description'])
                            genre_obj.save()

                    # Категории
                    for category in self.object['categories']:
                        category_obj = Category.objects.filter(name=category['description']).first()
                        if not category_obj:
                            category_obj = Category(name=category['description'])
                            category_obj.save()
            else:
                print(f'Ошибка получения данных', file=sys.stderr)

        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.is_full_data:
            context['developers'] = ','.join(self.object['developers'])
            context['publishers'] = ','.join(self.object['publishers'])
            self.is_full_data = False

        return context
