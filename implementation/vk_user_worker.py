"""
модуль нижнего уровня, который реализует получение данных о пользователе из сервиса вк 
"""
__author__ = 'Korovaev A.V.'


import vk
import time
import asyncio
from datetime import datetime
from interfaces.i_user_worker import IUserWorker


class VKUserWorker(IUserWorker):
    def __init__(self, token, api_version):
        self.token = token
        self.api_version = api_version

    async def get_user_by_id(self, user_id):
        """
        асинхронная обёртка метода для получения данных о пользователе
        :param user_id: id пользователя данные о котором необходимо получить
        """
        print(f'start get id at {datetime.now().time()}\n')
        def get_user_by_id_vk(user_id):
            """
            метод для получения данных о пользователе из вк
            :param user_id: id пользователя данные о котором необходимо получить
            """
            print(f'start vk at {datetime.now().time()}\n')
            session = vk.Session(access_token=self.token)
            api = vk.API(session, v=self.api_version)
            time.sleep(1)
            profile_info = api.account.getProfileInfo()
            print(f'finish vk at {datetime.now().time()}\n')
            return profile_info

        async def make_coro(future):
            try:
                return await future
            except asyncio.CancelledError:
                return await future
        print(f'start executor at {datetime.now().time()}\n')
        future = asyncio.get_running_loop().run_in_executor(None, get_user_by_id_vk, (user_id,))
        print(f'start task at {datetime.now().time()}\n')
        task = await asyncio.create_task(make_coro(future))
        print(f'finish get id at {datetime.now().time()}\n')
        return task
