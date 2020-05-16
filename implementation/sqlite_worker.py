"""
    Модуль является низкоуровневым и описывает способ получения данных из БД SQLite
"""
__author__ = 'Korovaev A.V.'


import aiosqlite
import time


class SQLiteWorker:

    def __new__(cls, db_name=None):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SQLiteWorker, cls).__new__(cls)
        if not hasattr(cls, 'db_name'):
            cls.db_name = db_name
        return cls.instance
    
    async def get_user_by_id(self, user_id):
        """
        метод для получения пользователя по его id
        :param user_id: id пользователя данные о котором необходимо получить
        """
        async with aiosqlite.connect(self.db_name) as conn:
            conn.row_factory = aiosqlite.Row
            async with conn.cursor() as cur:
                await cur.execute('SELECT * FROM user_info WHERE "user_id"=?',(user_id,))
                rez = await cur.fetchone()
                return dict(rez) if rez is not None else rez

    async def get_vk_connect_data(self, vk_id):
        """
        метод для получения данных подключения к сервису контакта
        :param vk_id: id учётной записи
        """
        async with aiosqlite.connect(self.db_name) as conn:
            conn.row_factory = aiosqlite.Row
            async with conn.cursor() as cur:
                await cur.execute('SELECT * FROM vk_connection WHERE "vk_id"=?',(vk_id,))
                rez = await cur.fetchone()
                return dict(rez) if rez is not None else rez

    async def save_user_data(self, user_data):
        """
        метод для получения пользователя по его id
        :param user_data: данные о пользователе, которые необходимо сохранить
        """
        async with aiosqlite.connect(self.db_name) as conn:
            async with conn.cursor() as cur:
                await cur.execute('INSERT INTO user_info VALUES(?, ?, ?, ?, ?)',
                                  (user_data.get('user_id'),
                                   user_data.get('name'),
                                   user_data.get('surname'),
                                   user_data.get('countries'),
                                   user_data.get('phone_number')))
                await conn.commit()