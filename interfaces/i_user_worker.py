"""
    Интерфейс, содержащий базовый функционал для получения данных пользователей.
    Служит прослойкой между модулями высокого и низкого уровня для обеспечения более слобой связности и удобного
    расширения функционала.
"""
__author__ = 'Korovaev A.V.'


class IUserWorker:

    def get_user_by_id(self, user_id):
        """
        получить данные пользователя
        :param user_id: id пользователя данные о котором необходимо получить
        """
        raise NotImplementedError