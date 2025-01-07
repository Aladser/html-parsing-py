import sys
from typing import Union

from bs4 import BeautifulSoup

from config.settings import MEDIA_ROOT


def get_games_info(file_path: str)-> Union[list, None]:
    """Возвращает информацию об играх"""

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        soup = BeautifulSoup(html_content, 'html.parser')
    except FileNotFoundError:
        print(f"Ошибка: Файл {file_path} не существует", file=sys.stderr)
        return None

    games_list = []
    elements = soup.find_all('tr', class_='app')
    for el in elements:
        td_list = el.find_all('td')
        # изображение
        image_src = td_list[1].find('img')['src']
        image_src_list = image_src.split('/')
        image_src = f"/media/site/index/{image_src_list[2]}"
        # время
        time = td_list[5].text.strip()
        if 'm' in time:
            time = time.replace('m', '')
            time = round(int(time) / 60, 2)
        elif time == '-':
            time = 0
        else:
            time = float(time.replace('h', ''))
        # цена
        price = td_list[4].text.strip().replace('No Price', '')
        if 'Not in Store' in price:
            price = ''
        # рейтинг
        rating = td_list[6].text.strip().replace('-', '')

        game = {
            'appid': el['data-appid'],
            'name': td_list[2].text.strip(),
            'price': price,
            'time': time,
            'rating': rating,
            'image': image_src
        }
        games_list.append(game)

    return games_list
