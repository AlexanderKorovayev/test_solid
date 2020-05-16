import asyncio
import time
from datetime import datetime, date
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from implementation import api


def do_something():
    print('start something')
    time.sleep(2)
    print('finish something')


async def get_user_by_id(user_id):
    """
    функция получения данных пользователя
    :param user_id: id пользователя данные о котором необходимо получить
    """

    # если данные о пользователе уже есть в базе данных то получим их
    # данный вариант с последовательным выполнением занимает
    # spend 0:00:02.037002 если не включать слипов
    # spend 0:00:05.039119 если включить слип на общение с базой 3 секунды
    # spend 0:00:00.044010 время которое тратится на запрос к бд
    user_data = await api.get_user_by_id_db(user_id)
    print(user_data)
    #do_something()
    
    if user_data['user_id'] != None:
        # проверяем корректность данных и возвращаем
        return user_data
    else:
        # получаем данные из вк
        user_data = await api.get_user_by_id_vk(user_id)
        print('from vk ' + str(user_data))
        # пишем в базу
        await api.save_user_data_pg(user_data)
        return user_data


async def main(user_id):
    """
    входная точка основного цикла событий
    """
    res = await get_user_by_id(user_id)
    return res


if __name__ == '__main__':
    print(asyncio.run(main(7396173)))
