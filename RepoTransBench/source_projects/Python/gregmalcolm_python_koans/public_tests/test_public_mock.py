import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from libs import mock

class TestPublicMockExample(unittest.TestCase):
    def test_public_basic_mock(self):
        m = mock.Mock()
        self.assertIsInstance(m, mock.Mock)
        m.hello = lambda: "moon"
        self.assertEqual(m.hello(), "moon")

    def test_public_side_effect(self):
        val = []
        m = mock.Mock(side_effect=lambda: val.append("invoked"))
        m()
        self.assertIn("invoked", val)

    def test_public_call_args(self):
        m = mock.Mock()
        m("b", c="y")
        self.assertEqual(m.call_args[0][0], "b")
        self.assertEqual(m.call_args[1]['c'], "y")

    def test_public_mock_return_value(self):
        m = mock.Mock(return_value=55)
        self.assertEqual(m(), 55)
        m.return_value = 23
        self.assertEqual(m(), 23)

    def test_public_mock_reset(self):
        m = mock.Mock()
        m('b')
        self.assertTrue(m.called)
        m.reset_mock()
        self.assertFalse(m.called)

class TestPublicMockCalls(unittest.TestCase):
    def test_public_multiple_calls(self):
        m = mock.Mock()
        m(11)
        m(22)
        self.assertEqual(m.call_count, 2)
        self.assertEqual(m.call_args_list[0][0], (11,))
        self.assertEqual(m.call_args_list[1][0], (22,))

    def test_public_assert_called_with(self):
        m = mock.Mock()
        m(999, z=888)
        m.assert_called_with(999, z=888)