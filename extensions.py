import requests
import json


class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            amount = float(amount)
        except ValueError:
            raise APIException("Количество должно быть числом.")

        if base == quote:
            raise APIException(f"Валюты {base} и {quote} идентичны. Смените одну из валют.")

        try:
            response = requests.get(f"https://api.exchangerate-api.com/v4/latest/{base}")
            data = response.json()
        except Exception as e:
            raise APIException(f"Ошибка при обращении к валютному сервису: {str(e)}")

        if quote not in data['rates']:
            raise APIException(f"Валюта {quote} не найдена.")

        if base not in data['rates']:
            raise APIException(f"Валюта {base} не найдена.")

        rate = data['rates'][quote]
        result = rate * amount

        return round(result, 2)