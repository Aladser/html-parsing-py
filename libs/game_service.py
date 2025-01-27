from libs.exchange_rate import ExchangeRate


class GameService:
    @staticmethod
    def add_game():
        KZT_RATING = ExchangeRate.get('Тенге')
