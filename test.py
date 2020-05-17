import unittest
import asyncio
from implementation import api


class QueryTest(unittest.TestCase):

    def setUp(self):
        self.incorrect_user_id = 739617333
        self.correct_user_id = 7396173
        self.correct_answer = {'user_id': 7396173,
                               'name': 'Александр',
                               'surname': 'Короваев',
                               'countries': 'Россия',
                               'phone_number': '+7 *** *** ** 63'}
        self.incorrect_answer = {'user_id': None,
                                 'name': None,
                                 'surname': None,
                                 'countries': None,
                                 'phone_number': None}
    
    async def test_get_user_by_id_db_incorrect(self):
        res = await api.get_user_by_id_db(self.incorrect_user_id)
        self.assertEqual(self.incorrect_answer, res)

    async def test_get_user_by_id_db_correct(self):
        res = await api.get_user_by_id_db(self.correct_user_id)
        self.assertEqual(self.correct_answer, res)
    
    async def test_get_user_by_id_vk_correct(self):
        res = await api.get_user_by_id_vk(self.correct_user_id)
        self.assertEqual(self.correct_answer, res)
    

async def main():
    await unittest.main()

if __name__ == '__main__':
    asyncio.run(main())
