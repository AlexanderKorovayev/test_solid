"""
модуль нижнего уровня, который реализует получение данных о пользователе в соответствии с заданным интерфейсом
по работе с базами данных 
"""
__author__ = 'Korovaev A.V.'


from interfaces.i_user_worker import IUserWorker
from implementation.sqlite_worker import SQLiteWorker


class SQLiteUserWorker(IUserWorker):
    async def get_user_by_id(self, user_id):
        """
        метод для получения данных о пользователе
        :param user_id: id пользователя данные о котором необходимо получить
        """
        sqlite_worker = SQLiteWorker()
        return await sqlite_worker.get_user_by_id(user_id)
