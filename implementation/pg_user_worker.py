"""
модуль нижнего уровня, который реализует получение данных о пользователе в соответствии с заданным интерфейсом
по работе с базами данных 
"""
__author__ = 'Korovaev A.V.'


from interfaces.i_user_worker import IUserWorker
from implementation.pg_worker import PGWorker


class PGUserWorker(IUserWorker):

    def __init__(self, db_name, login, password, host='localhost', port='5432'):
        self.db_name = db_name
        self.login = login
        self.password = password
        self.host = host
        self.port = port

    def get_user_by_id(self, user_id):
        """
        метод для получения данных о пользователе
        :param user_id: id пользователя данные о котором необходимо получить
        """

        pg_worker = PGWorker(self.db_name, self.login, self.password, self.host, self.port)
        return pg_worker.get_user_by_id(user_id)
