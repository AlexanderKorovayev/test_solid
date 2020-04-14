"""
    Модуль является низкоуровневым и описывает способ получения данных из БД Postgres
"""
__author__ = 'Korovaev A.V.'


import psycopg2
from psycopg2.extras import DictCursor
from interfaces.i_db_worker import IDBWorker


class PGWorker(IDBWorker):

    def __init__(self, db_name, login, password, host='localhost', port='5432'):
        self.db_name = db_name
        self.login = login
        self.password = password
        self.host = host
        self.port = port
    
    def get_user_by_id(self, user_id):
        """
        метод для получения пользователя по его id
        :param user_id: id пользователя данные о котором необходимо получить
        """

        conn = psycopg2.connect(database=self.db_name,
                                user=self.login,
                                password=self.password,
                                host=self.host,
                                port=self.port)
        
        with conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute('SELECT * FROM user_info WHERE "user_id"=%s',(user_id,))
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
                             user_data.get('first_name'),
                             user_data.get('last_name'),
                             user_data.get('country'),
                             user_data.get('phone')))






