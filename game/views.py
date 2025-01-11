import sys

from django.views.generic import DetailView
from django.views.generic import ListView

from config.settings import STEAM_API_KEY
from game.models import Game, Developer, Publisher
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
                    print(self.object['genres'])
                    print(self.object['categories'])
                    print(self.object['header_image'])
                    print(self.object['background'])

                    print("Разработчики:")
                    for developer in self.object['developers']:
                        print(developer, end="(")
                        developer_obj = Developer.objects.filter(name=developer).first()
                        print(developer_obj is not None, end=")\n")
                        if not developer_obj:
                            developer_obj = Developer(name=developer)
                            developer_obj.save()

                    print("Издатели:")
                    for publisher in self.object['publishers']:
                        print(publisher, end="(")
                        publisher_obj = Publisher.objects.filter(name=developer).first()
                        print(publisher_obj is not None, end=")\n")
                        if not publisher_obj:
                            publisher_obj = Publisher(name=publisher)
                            publisher_obj.save()

                    print("Жанры:")

                    print("Категории:")
                    """
                        developers = models.ManyToManyField(Developer, verbose_name="Разработчики", **NULLABLE)
                        publishers = models.ManyToManyField(Publisher, verbose_name="Издатели", **NULLABLE)
                        genres = models.ManyToManyField(Genre, verbose_name="Жанры", **NULLABLE)
                        categories = models.ManyToManyField(Category, verbose_name="Категории", **NULLABLE)
                    """
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
