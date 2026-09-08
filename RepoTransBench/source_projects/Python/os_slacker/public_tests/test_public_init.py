import unittest
import json
import types
from unittest.mock import patch, MagicMock

from slacker import (
    Error, Response, BaseAPI, API, Auth
)

class TestResponsePublic(unittest.TestCase):
    def test_successful_response(self):
        body = json.dumps({'ok': True, 'value': 100})
        resp = Response(body)
        self.assertTrue(resp.successful)
        self.assertEqual(resp.body['value'], 100)
        self.assertIsNone(resp.error)
        self.assertIn('"value": 100', str(resp))

    def test_error_response(self):
        body = json.dumps({'ok': False, 'error': 'otherfail'})
        resp = Response(body)
        self.assertFalse(resp.successful)
        self.assertEqual(resp.error, 'otherfail')
        self.assertIn('otherfail', str(resp))

class TestBaseAPIPublic(unittest.TestCase):
    @patch('slacker.get_api_url', lambda m: f'https://slack.com/api/{m}')
    @patch('requests.get')
    def test_get_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = json.dumps({'ok': True, 'x': 5})
        mock_get.return_value = mock_response

        api = BaseAPI(token='another_test')
        resp = api.get('api.other_test')
        self.assertTrue(resp.successful)

    @patch('slacker.get_api_url', lambda m: f'https://slack.com/api/{m}')
    @patch('requests.get')
    def test_get_error(self, mock_get):
        # Test raising error if ok: False
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = json.dumps({'ok': False, 'error': 'badrequest'})
        mock_get.return_value = mock_response

        api = BaseAPI(token='another_test')
        with self.assertRaises(Error) as cm:
            api.get('api.other_test')
        self.assertEqual(str(cm.exception), 'badrequest')

    @patch('slacker.get_api_url', lambda m: f'https://slack.com/api/{m}')
    @patch('requests.get')
    def test_get_429_retry(self, mock_get):
        # simulate 429, then success
        state = {}
        def fake_get(url, timeout, proxies=None, **kwargs):
            if not state.get('retried'):
                state['retried'] = True
                resp = MagicMock()
                resp.status_code = 429
                resp.headers = {'retry-after': '1'}
                return resp
            # next retry: success
            resp = MagicMock()
            resp.status_code = 200
            resp.text = json.dumps({'ok': True})
            return resp
        mock_get.side_effect = fake_get

        api = BaseAPI(token='another_test', rate_limit_retries=2)
        with patch('time.sleep') as mock_sleep:
            resp = api.get('api.other_test')
            self.assertTrue(resp.successful)
            mock_sleep.assert_called_with(1)

    @patch('slacker.get_api_url', lambda m: f'https://slack.com/api/{m}')
    def test_session_methods(self):
        fake_session = MagicMock()
        api = BaseAPI(token='another_test', session=fake_session)
        url = 'http://another-url'
        # _session_get
        api._session_get(url, params={'x': 10})
        fake_session.request.assert_called_with(method='get', url=url, params={'x': 10}, allow_redirects=True)
        # _session_post
        api._session_post(url, data={'y': 20})
        fake_session.request.assert_called_with(method='post', url=url, data={'y': 20})

class TestAPIPublic(unittest.TestCase):
    @patch.object(BaseAPI, 'get')
    def test_api_test(self, mock_get):
        api = API(token='T_public')
        api.test()
        api.test(error='badrequest', x=42)
        self.assertTrue(mock_get.called)

class TestAuthPublic(unittest.TestCase):
    @patch.object(BaseAPI, 'get')
    def test_auth_test(self, mock_get):
        auth = Auth(token='T_public')
        auth.test()
        mock_get.assert_called_with('auth.test')

    @patch.object(BaseAPI, 'post')
    def test_auth_revoke(self, mock_post):
        auth = Auth(token='T_public')
        auth.revoke()
        auth.revoke(test=False)
        calls = mock_post.call_args_list
        self.assertEqual(calls[0][0][0], 'auth.revoke')
        self.assertEqual(calls[0][1]['data'], {'test': 1})
        self.assertEqual(calls[1][1]['data'], {'test': 0})

class TestErrorPublic(unittest.TestCase):
    def test_error_repr(self):
        e = Error('another error message')
        self.assertEqual(str(e), 'another error message')