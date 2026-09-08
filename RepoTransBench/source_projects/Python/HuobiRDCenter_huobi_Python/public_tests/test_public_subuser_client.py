import unittest
from unittest.mock import patch, MagicMock
import sys

# Provide a separate dummy scenario for public tests
class DummySubuserClientPublic:
    def __init__(self, api_key=None, secret_key=None):
        self.api_key = api_key
        self.secret_key = secret_key

    def post_set_subuser_transferability(self, sub_uids, transferability):
        if sub_uids is None:
            raise ValueError("sub_uids required")
        if isinstance(transferability, bool):
            # Use different values for sub_uids, True/False logic is same
            return [{"uid": sub_uids, "success": True, "transferability": transferability}]
        else:
            raise TypeError("transferability must be bool")

    def get_sub_user_deposit_history(self, sub_uid=None):
        # Simulate success and error with different sub_uid for error
        if sub_uid == -1:
            raise Exception("Not found")
        class Result:
            def print_object(self):
                return "done"
        return Result()

    def post_subuser_apikey_generate(self, otp_token, sub_uid, note, permission):
        # Simple validator
        if not otp_token or not note:
            raise ValueError("otp_token and note required")
        class Result:
            def print_object(self):
                return "done"
        return Result()

# Mock import paths for huobi.client.subuser
sys.modules['huobi.client.subuser'] = MagicMock()
sys.modules['huobi.constant'] = MagicMock()
sys.modules['huobi.utils'] = MagicMock()

from huobi.client import subuser

subuser.SubuserClient = DummySubuserClientPublic

class TestSubuserClientPublicIntegration(unittest.TestCase):
    def setUp(self):
        self.client = DummySubuserClientPublic(api_key="public-key", secret_key="public-secret")

    def test_post_set_subuser_transferability_true(self):
        res = self.client.post_set_subuser_transferability('abcd', True)
        self.assertIsInstance(res, list)
        self.assertEqual(res[0]['transferability'], True)
        self.assertEqual(res[0]['uid'], 'abcd')

    def test_post_set_subuser_transferability_false(self):
        res = self.client.post_set_subuser_transferability('efgh', False)
        self.assertEqual(res[0]['transferability'], False)

    def test_post_set_subuser_transferability_invalid(self):
        with self.assertRaises(TypeError):
            self.client.post_set_subuser_transferability('efgh', 123)

    def test_post_set_subuser_transferability_no_uid(self):
        with self.assertRaises(ValueError):
            self.client.post_set_subuser_transferability(None, True)

    def test_get_sub_user_deposit_history_ok(self):
        res = self.client.get_sub_user_deposit_history(sub_uid=555)
        self.assertTrue(hasattr(res, 'print_object'))
        self.assertEqual(res.print_object(), "done")

    def test_get_sub_user_deposit_history_not_found(self):
        with self.assertRaises(Exception):
            self.client.get_sub_user_deposit_history(sub_uid=-1)

    def test_post_subuser_apikey_generate_success(self):
        res = self.client.post_subuser_apikey_generate('pub_otp', 999, 'pub_note', 'readWrite')
        self.assertTrue(hasattr(res, 'print_object'))
        self.assertEqual(res.print_object(), "done")

    def test_post_subuser_apikey_generate_missing(self):
        with self.assertRaises(ValueError):
            self.client.post_subuser_apikey_generate('', 999, '', 'readWrite')

    def test_init(self):
        c = DummySubuserClientPublic()
        self.assertIsNone(c.api_key)
        self.assertIsNone(c.secret_key)

if __name__ == '__main__':
    unittest.main()