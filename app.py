import time
from datetime import datetime, date
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from implementation import api


def do_something():
    print('start something')
    time.sleep(2)
    print('finish something')


def get_user_by_id(user_id):
    """
    функция получения данных пользователя
    :param user_id: id пользователя данные о котором необходимо получить
    """

    # если данные о пользователе уже есть в базе данных то получим их
    # данный вариант с последовательным выполнением занимает
    # spend 0:00:02.037002 если не включать слипов
    # spend 0:00:05.039119 если включить слип на общение с базой 3 секунды
    # spend 0:00:00.044010 время которое тратится на запрос к бд
    '''
    start_time = datetime.now().time()
    user_data = api.get_user_by_id_db(user_id)
    do_something()
    print('from bd ' + str(user_data))
    print(f'spend {datetime.combine(date.today(), datetime.now().time()) - datetime.combine(date.today(), start_time)}')
    '''
    # в случае с выделением отдельного потока для общения с базой
    # spend 0:00:02.017477 если не включать слипов
    # spend 0:00:03.292588 если включить слип на общение с базой 3 секунды
    # spend 0:00:00.044010 время которое тратится на запрос к бд
    start_time = datetime.now().time()
    with ProcessPoolExecutor(max_workers=1) as executor:
        print(f'in {multiprocessing.current_process().name} at {datetime.now().time()}\n')
        ex_obj = executor.submit(api.get_user_by_id_db, user_id)
        print(f'in {multiprocessing.current_process().name} at {datetime.now().time()}\n')
        # пока запрос к базе выполянется сделаем ещё некоторую работу
        if not ex_obj.done():
            do_something()
        user_data = ex_obj.result()
        print('from bd ' + str(user_data))
    print(f'spend {datetime.combine(date.today(), datetime.now().time()) - datetime.combine(date.today(), start_time)}')
    
    if user_data['user_id'] != None:
        # проверяем корректность данных и возвращаем
        return user_data
    else:
        # получаем данные из вк
        user_data = api.get_user_by_id_vk(user_id)
        print('from vk ' + str(user_data))
        # пишем в базу
        api.save_user_data_pg(user_data)
        return user_data


if __name__ == '__main__':
    get_user_by_id(7396173)
