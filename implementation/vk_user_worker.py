"""
модуль нижнего уровня, который реализует получение данных о пользователе из сервиса вк 
"""
__author__ = 'Korovaev A.V.'


import vk
from interfaces.i_user_worker import IUserWorker


class VKUserWorker(IUserWorker):

    def __init__(self, token, api_version):
        self.token = token
        self.api_version = api_version

    def get_user_by_id(self, user_id):
        """
        метод для получения данных о пользователе
        :param user_id: id пользователя данные о котором необходимо получить
        """

        session = vk.Session(access_token=self.token)
        api = vk.API(session, v=self.api_version)
        profile_info = api.account.getProfileInfo()
        return profile_info
