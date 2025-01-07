from bs4 import BeautifulSoup

# Открываем локальный HTML-файл
with open('index.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Создаем объект BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Пример: Извлечение заголовков h1 и h2
h1_headers = soup.find_all('h1')
h2_headers = soup.find_all('h2')

print("Заголовки h1:")
for header in h1_headers:
    print(header.text)

print("\nЗаголовки h2:")
for header in h2_headers:
    print(header.text)

# Пример: Извлечение всех ссылок
print("\nСсылки:")
links = soup.find_all('a')
for link in links:
    print(link.get('href'))