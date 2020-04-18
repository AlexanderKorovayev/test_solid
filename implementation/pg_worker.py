"""
    Модуль является низкоуровневым и описывает способ получения данных из БД Postgres
"""
__author__ = 'Korovaev A.V.'


import psycopg2
from psycopg2.extras import DictCursor
import time


class PGWorker:

    def __new__(cls, db_name=None, login=None, password=None, host='localhost', port='5432'):
        if not hasattr(cls, 'instance'):
            cls.instance = super(PGWorker, cls).__new__(cls)
        if not hasattr(cls, 'db_name'):
            cls.db_name = db_name
        if not hasattr(cls, 'login'):
            cls.login = login
        if not hasattr(cls, 'password'):
            cls.password = password
        if not hasattr(cls, 'host'):
            cls.host = host
        if not hasattr(cls, 'port'):
            cls.port = port
        return cls.instance
    
    def get_user_by_id(self, user_id):
        """
        метод для получения пользователя по его id
        :param user_id: id пользователя данные о котором необходимо получить
        """

        print('in')
        conn = psycopg2.connect(database=self.db_name,
                                user=self.login,
                                password=self.password,
                                host=self.host,
                                port=self.port)
        
        with conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute('SELECT * FROM user_info WHERE "user_id"=%s',(user_id,))
                time.sleep(3)
                rez = cur.fetchone()
                return dict(rez) if rez is not None else rez

    def get_vk_connect_data(self, vk_id):
        """
        метод для получения данных подключения к сервису контакта
        :param vk_id: id учётной записи
        """

        conn = psycopg2.connect(database=self.db_name,
                                user=self.login,
                                password=self.password,
                                host=self.host,
                                port=self.port)
        
        with conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute('SELECT * FROM vk_connection WHERE "vk_id"=%s',(vk_id,))
                rez = cur.fetchone()
                return dict(rez) if rez is not None else rez

    def save_user_data(self, user_data):
        """
        метод для получения пользователя по его id
        :param user_data: данные о пользователе, которые необходимо сохранить
        """

        conn = psycopg2.connect(database=self.db_name,
                                user=self.login,
                                password=self.password,
                                host=self.host,
                                port=self.port)
        
        with conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute('INSERT INTO user_info VALUES(%s, %s, %s, %s, %s)',
                            (user_data.get('user_id'),
                             user_data.get('name'),
                             user_data.get('surname'),
                             user_data.get('countries'),
                             user_data.get('phone_number')))
