import unittest
from sample import core
from sample import helpers

class TestCore(unittest.TestCase):

    def test_get_hmm(self):
        self.assertEqual(core.get_hmm(), 'hmmm...')

    def test_hmm_true(self):
        # get_answer returns True: should print 'hmmm...'
        # To capture print output, need to redirect stdout
        import io
        import sys
        captured_output = io.StringIO()
        sys_stdout = sys.stdout
        sys.stdout = captured_output
        try:
            core.hmm()
        finally:
            sys.stdout = sys_stdout
        output = captured_output.getvalue().strip()
        self.assertEqual(output, 'hmmm...')

    def test_hmm_false(self):
        # Patch helpers.get_answer to False
        import io
        import sys
        from unittest.mock import patch
        captured_output = io.StringIO()
        sys_stdout = sys.stdout
        sys.stdout = captured_output
        try:
            with patch('sample.helpers.get_answer', return_value=False):
                core.hmm()  # Should not print anything
        finally:
            sys.stdout = sys_stdout
        output = captured_output.getvalue().strip()
        self.assertEqual(output, '')

class TestHelpers(unittest.TestCase):

    def test_get_answer(self):
        # should always return True
        self.assertTrue(helpers.get_answer())