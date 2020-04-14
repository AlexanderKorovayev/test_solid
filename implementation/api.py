"""
модуль содержит api для работы с пользователями, т.е. является модулем верхнего уровня, который реализует бизнес логику
"""
__author__ = 'Korovaev A.V.'

from implementation.pg_worker import PGWorker
from implementation.transport import UserTransport
from implementation.pg_user_worker import PGUserWorker
from implementation.vk_user_worker import VKUserWorker


def get_user_by_id(user_id):
    """
    функция получения данных пользователя
    :param user_id: id пользователя данные о котором необходимо получить
    """

    pg_user_worker = PGUserWorker(db_name='test_solid', login='postgres', password='postgres')
    user_transport = UserTransport(pg_user_worker)
    # если данные о пользователе уже есть в базе данных то получим их
    user_data = user_transport.get_user_by_id(user_id)
    print('from bd ' + str(user_data))
    if user_data:
        # проверяем корректность данных и возвращаем
        return user_data
    else:
        # получаем данные для подключения к вк
        # сделать работу с базами синглтоном
        pg_worker = PGWorker(db_name='test_solid', login='postgres', password='postgres')
        connection_data = pg_worker.get_vk_connect_data('7396173')
        # проверяем корректность данных и если всё норм то получаем данные из вк
        token = connection_data.get('access_token')
        api_version = connection_data.get('v')
        vk_user_worker = VKUserWorker(token, api_version)
        user_transport = UserTransport(vk_user_worker)
        user_data = user_transport.get_user_by_id(user_id)
        # формируем нужный формат
        res = {k: v.get('title') if k=='country' else v for k, v in user_data.items() if k in
               ('first_name', 'last_name', 'phone', 'country')}
        res['user_id'] = user_id
        print('from vk ' + str(res))
        # пишем в базу
        pg_worker.save_user_data(res)
        return res
        # в этом модуле мы уже делаем проверки на корректность данных и прочее а так же предаставляем бизнес логику
        # дальше модуль маин уже использует то что нужно конкретным задачам того кто хочет использвать наш апи
