from implementation import api


def get_user_by_id(user_id):
    """
    функция получения данных пользователя
    :param user_id: id пользователя данные о котором необходимо получить
    """

    # если данные о пользователе уже есть в базе данных то получим их
    user_data = api.get_user_by_id_db(user_id)
    print('from bd ' + str(user_data))
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


get_user_by_id(7396173)