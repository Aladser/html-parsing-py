from game.models import Game, Developer, Publisher, Genre, Category


class GameService:
    """
    object.background background
    object.id id
    object.name name
    object.header_image header_image
    object.short_description short_description
    object.metacritic
        object.metacritic.url metacritic_link
        object.metacritic.score metacritic
    object.release_date release_date
    """
    @staticmethod
    def insert_game(game_object):
        game_param_list = {
            "id": game_object["steam_appid"],
            "name": game_object["name"],
            "header_image": game_object["header_image"],
            "short_description": game_object["short_description"],
            "metacritic": game_object["metacritic"]['score'] if "metacritic" in game_object else 0,
            "metacritic_link": game_object["metacritic"]['url'] if "metacritic" in game_object else None,
            "release_date": game_object["release_date"]['date'],
            "background": game_object["background"],
            "price": game_object["price"] if "price" in game_object else None,
            'is_free': game_object["is_free"]
        }
        game = Game.objects.create(**game_param_list)

        # Разработчики
        for developer in game_object['developers']:
            developer_obj = Developer.objects.filter(name=developer).first()
            if not developer_obj:
                developer_obj = Developer(name=developer)
                developer_obj.save()
            game.developers.add(developer_obj)

        # Издатели
        for publisher in game_object['publishers']:
            publisher_obj = Publisher.objects.filter(name=publisher).first()
            if not publisher_obj:
                publisher_obj = Publisher(name=publisher)
                publisher_obj.save()
            game.publishers.add(publisher_obj)

        # Жанры
        for genre in game_object['genres']:
            genre_obj = Genre.objects.filter(name=genre['description']).first()
            if not genre_obj:
                genre_obj = Genre(name=genre['description'])
                genre_obj.save()
            game.genres.add(genre_obj)

        # Категории
        for category in game_object['categories']:
            category_obj = Category.objects.filter(name=category['description']).first()
            if not category_obj:
                category_obj = Category(name=category['description'])
                category_obj.save()
            game.categories.add(category_obj)

        return game
