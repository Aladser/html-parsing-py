from django.core.management import BaseCommand

from game.models import Game
from libs.seeding import Seeding


class Command(BaseCommand):
    game_list = [
        {'id': 1,
         'name': 'name',
         'short_description': 'short_description',
         'metacritic': 5,
         'metacritic_link': 'metacritic_link',
         'release_date': 'release_date',
         'developers': 'developers',
         'publishers': 'publishers',
         'genres': 'genres',
         'categories': 'categories',
         'header_image': 'header_image',
         'background': 'background'
         },
        {'id': 2,
         'name': 'name2',
         'short_description': 'short_description2',
         'metacritic': 4,
         'metacritic_link': 'metacritic_link2',
         'release_date': 'release_date2',
         'developers': 'developer2',
         'publishers': 'publishers2',
         'genres': 'genres2',
         'categories': 'categories2',
         'header_image': 'header_image2',
         'background': 'background2'
        },
        {'id': 3,
         'name': 'name3',
         'short_description': 'short_description3',
         'metacritic': 3,
         'metacritic_link': 'metacritic_link3',
         'release_date': 'release_date3',
         'developers': 'developers3',
         'publishers': 'publishers3',
         'genres': 'genres3',
         'categories': 'categories3',
         'header_image': 'header_image3',
         'background': 'background3'
         }
    ]

    def handle(self, *args, **kwargs):
        Game.truncate()
        Seeding.seed_table(Game, self.game_list)
