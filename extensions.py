class APIException(Exception):
    pass

class InputException(APIException):
    def __str__(self):
        return('Ошибка ввода пользователя (неверное количество аргументов запроса)')

class CoinNotExist(APIException):
    pass

class SameCoins(APIException):
    def __str__(self):
        return('Невозможно конвертировать одинаковые валюты')

class WrongAmount(APIException):
    def __str__(self):
        return('Неверное количество валюты')