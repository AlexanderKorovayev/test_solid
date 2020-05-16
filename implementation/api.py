"""
модуль содержит api для работы с пользователями, т.е. является модулем верхнего уровня, который реализует бизнес логику
"""
__author__ = 'Korovaev A.V.'

import multiprocessing
from implementation.sqlite_worker import SQLiteWorker
from implementation.transport import UserTransport
from implementation.sqlite_user_worker import SQLiteUserWorker
from implementation.vk_user_worker import VKUserWorker


async def get_user_by_id_db(user_id):
    """
    функция получения данных пользователя из базы данных
    :param user_id: id пользователя данные о котором необходимо получить
    """
    # результат по умолчанию
    result = {'user_id': None, 'name': None, 'surname': None, 'countries': None, 'phone_number': None}

    # создаём синглтон для работы с базами данных
    sqlite_worker = SQLiteWorker(db_name='test_solid.db')

    # пробуем получить данные из базы
    sqlite_user_worker = SQLiteUserWorker()
    user_transport = UserTransport(sqlite_user_worker)
    # если данные о пользователе уже есть в базе данных то получим их
    user_data = await user_transport.get_user_by_id(user_id)
    
    if user_data:
        # проверяем корректность данных и возвращаем
        result = user_data
        return result
    else:
        return result


async def get_user_by_id_vk(user_id):
    """
    функция получения данных пользователя из червиса вк
    :param user_id: id пользователя данные о котором необходимо получить
    """

    # результат по умолчанию
    result = {'user_id': None, 'name': None, 'surname': None, 'countries': None, 'phone_number': None}

    # создаём синглтон для работы с базами данных
    sqlite_worker = SQLiteWorker(db_name='test_solid.db')

    # получаем данные для подключения к вк
    connection_data = await sqlite_worker.get_vk_connect_data(str(user_id))
    # проверяем корректность данных
    token = connection_data.get('access_token')
    api_version = connection_data.get('v')
    # если всё норм то получаем данные из вк
    vk_user_worker = VKUserWorker(token, api_version)
    user_transport = UserTransport(vk_user_worker)
    user_data = await user_transport.get_user_by_id(user_id)
    if user_data:
        # формируем нужный формат
        vk_result = {k: v.get('title') if k=='country' else v for k, v in user_data.items() if k in
                     ('first_name', 'last_name', 'phone', 'country')}
        result['user_id'] = user_id
        result['name'] = vk_result.get('first_name')
        result['surname'] = vk_result.get('last_name')
        result['countries'] = vk_result.get('country')
        result['phone_number'] = vk_result.get('phone')
        return result
    else:
        return result


async def save_user_data_pg(user_data):
    """
    функция сохранения данных в базу постгреса
    :param user_data: данные, которые необходимо сохранить
    """
    # проверяем что данные для записи корректны
    # создаём синглтон для работы с базами данных
    pg_worker = SQLiteWorker(db_name='test_solid.db')
    await pg_worker.save_user_data(user_data)
