import asyncio
import time
from datetime import datetime
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from implementation import api


async def some_work():
    print(f'I some work at {datetime.now().time()}\n')
    await asyncio.sleep(2)
    print(f'I some work again at {datetime.now().time()}\n')
    return 100


async def get_user_by_id(user_id):
    """
    функция получения данных пользователя
    :param user_id: id пользователя данные о котором необходимо получить
    """
    print(f'start get DB data {datetime.now().time()}')
    user_data = await api.get_user_by_id_db(user_id)
    if user_data['user_id'] != None:
        # проверяем корректность данных и возвращаем
        print(f'finish get DB data {datetime.now().time()}')
        return user_data
    else:
        # получаем данные из вк
        user_data = await api.get_user_by_id_vk(user_id)
        # пишем в базу
        await api.save_user_data_pg(user_data)
        return user_data


async def main(user_id):
    """
    входная точка основного цикла событий
    """
    # запустили таск на получение данных о пользователе
    db_task = asyncio.create_task(get_user_by_id(user_id))
    # выполним некоторую работу пока идёт запрос в бд
    print(f'I some work at {datetime.now().time()}\n')
    await asyncio.sleep(1.1)
    print(f'I some work again at {datetime.now().time()}\n')
    if not db_task.done():
        print('not finish task')
        await db_task
        res = db_task.result()
    res = db_task.result()
    return res


if __name__ == '__main__':
    print(asyncio.run(main(7396173)))
