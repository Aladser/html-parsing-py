from bs4 import BeautifulSoup
import requests

class ExchangeRate:
    @staticmethod
    def get(curname):
        soup = BeautifulSoup(requests.get('https://www.cbr.ru/currency_base/daily/').text, "html.parser")
        kzt_rating_list = soup.find(text=curname).parent.parent.select('td')
        kzt_rate_str = float(kzt_rating_list[4].text.replace(',', '.'))
        return round(kzt_rate_str / float(kzt_rating_list[2].text), 2)
