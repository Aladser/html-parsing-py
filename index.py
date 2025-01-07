from bs4 import BeautifulSoup

with open('./site/index.html', 'r', encoding='utf-8') as file:
    html_content = file.read()
soup = BeautifulSoup(html_content, 'html.parser')

games_list = []
elements = soup.find_all('tr', class_='app')
for el in elements:
    td_list = el.find_all('td')
    image_src = td_list[1].find('img')['src']
    image_src_list = image_src.split('/')
    image_src = f"./site/{image_src_list[2]}"
    game = {
        'name':td_list[2].text.strip(),
        'price': td_list[4].text.strip(),
        'time': td_list[5].text.strip(),
        'rating': td_list[6].text.strip(),
        'image': image_src
    }
    games_list.append(game)

[print(game) for game in games_list]
