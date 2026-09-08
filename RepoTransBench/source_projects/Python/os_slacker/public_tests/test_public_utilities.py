import unittest

from slacker.utilities import get_item_id_by_name

class TestGetItemIDByNamePublic(unittest.TestCase):
    def test_get_item_id_by_name(self):
        list_dict = [{'name': 'public_channel', 'id': '789'}, {'name': 'other', 'id': '456'}]
        self.assertEqual(
            '789', get_item_id_by_name(list_dict, 'public_channel')
        )