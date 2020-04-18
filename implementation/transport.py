"""
модуль осуществляющий мост между модулями высокого и низкого уровня, главная задача которого получить данные и
отправить их api
"""
__author__ = 'Korovaev A.V.'
from interfaces.i_user_worker import IUserWorker


class UserTransport:

    def __init__(self, low_lavel_obj):
        if not self.__check_type(low_lavel_obj, IUserWorker):
            raise Exception(f'{low_lavel_obj.__name__} no match to standart of {IUserWorker.__name__}')
        self.__low_lavel_obj = low_lavel_obj

    def get_user_by_id(self, user_id):
        """
        метод для получения данных о пользователе
        :param user_id: id пользователя данные о котором необходимо получить
        """
        user_getter = self.__low_lavel_obj
        return user_getter.get_user_by_id(user_id)

    def __check_type(self,low_lavel_obj, higth_lavel_obj):
        """
        Метод проверки соответсвия объекта базовому типу
        :param low_lavel_obj: объект, который необходимо проверить
        :param base_type: базовый тип
        :return: True or False
        """
        rez = False

        if type(low_lavel_obj) == type:
            rez_object = low_lavel_obj
        else:
            rez_object = low_lavel_obj.__class__

        if rez_object.__name__ == 'object':
            return rez
        for base in rez_object.__bases__:
            if base.__name__ == higth_lavel_obj.__name__:
                rez = True
                return rez
            else:
                rez = self.__check_type(base, higth_lavel_obj)
                if rez is True:
                    return rez
        return rez
  