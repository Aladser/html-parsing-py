import sys

from config.settings import MEDIA_ROOT
from main.services import get_games_info

games_list = get_games_info(str(MEDIA_ROOT) + '/site/index.html')
if games_list is None:
    sys.exit()

for game in games_list:
    game_info = f"{game['name']}: время {game['time']}ч, "
    if game['price'] != '':
        game_info += f"цена {game['price']}, "
    if game['rating'] != '':
        game_info += f"рейтинг {game['rating']}, "
    game_info += f"лого  \"{game['image']}\""
    print(game_info)
