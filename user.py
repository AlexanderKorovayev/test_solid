"""
    Модуль описывает возможные контейнеры ждя хранения информации о пользователе
"""
__author__ = 'Korovaev A.V.'


import random


class User:
    """
    класс контейнер, для обработки информации о пользователе
    """

    user_count = random.randint(0, 1000000)

    def __init__(self, user_data: dict):
        self.name = user_data.get('name') or f'name_{User.user_count}'
        self.surname = user_data.get('surname') or f'surname_{User.user_count}'
        self.countries = user_data.get('countries') or f'countries_{User.user_count}'
        self.__number = user_data.get('number') or f'number_{User.user_count}'

    def get_number(self):
        return ''.join([el if el not in ['3', '4', '5'] else '*' for el in self.__number])
    
    def __str__(self):
        return f'User {self.name} {self.surname} from {self.countries}, number phone {self.get_number()}'

