import sys
from unittest import TestCase, skipUnless

try:
    from unittest.mock import patch, Mock
except ImportError:
    from mock import patch, Mock

from colorama.ansitowin32 import StreamWrapper
from colorama.initialise import init, just_fix_windows_console, _wipe_internal_state_for_tests

import colorama.tests.utils as test_utils

orig_stdout = sys.stdout
orig_stderr = sys.stderr

class PublicInitTest(TestCase):

    @skipUnless(sys.stdout.isatty(), "sys.stdout is not a tty")
    def setUp(self):
        self.assertNotWrapped()

    def tearDown(self):
        _wipe_internal_state_for_tests()
        sys.stdout = orig_stdout
        sys.stderr = orig_stderr

    def assertWrapped(self):
        self.assertIsNot(sys.stdout, orig_stdout, 'stdout should be wrapped')
        self.assertIsNot(sys.stderr, orig_stderr, 'stderr should be wrapped')
        self.assertTrue(isinstance(sys.stdout, StreamWrapper),
            'bad stdout wrapper')
        self.assertTrue(isinstance(sys.stderr, StreamWrapper),
            'bad stderr wrapper')

    def assertNotWrapped(self):
        self.assertIs(sys.stdout, orig_stdout, 'stdout should not be wrapped')
        self.assertIs(sys.stderr, orig_stderr, 'stderr should not be wrapped')

    @patch('colorama.initialise.reset_all')
    @patch('colorama.ansitowin32.winapi_test', lambda *_: True)
    @patch('colorama.ansitowin32.enable_vt_processing', lambda *_: True)
    def testInitWrapsOnWindows_public(self, _):
        with test_utils.osname("nt"):
            init()
            self.assertWrapped()

    @patch('colorama.initialise.reset_all')
    @patch('colorama.ansitowin32.winapi_test', lambda *_: False)
    def testInitDoesntWrapOnEmulatedWindows_public(self, _):
        with test_utils.osname("nt"):
            init(autoreset=False)
            self.assertNotWrapped()

    def testInitDoesntWrapOnNonWindows_public(self):
        with test_utils.osname("java"):
            init()
            self.assertNotWrapped()

    def testInitDoesntWrapIfNone_public(self):
        with test_utils.replace_by(None):
            init()
            self.assertIsNone(sys.stdout)
            self.assertIsNone(sys.stderr)

    def testInitAutoresetOnWrapsOnAllPlatforms_public(self):
        with test_utils.osname("customos"):
            init(autoreset=True)
            self.assertWrapped()

    def testInitWrapOffDoesntWrapOnWindows_public(self):
        with test_utils.osname("nt"):
            init(wrap=False)
            self.assertNotWrapped()

    def testInitWrapOffIncompatibleWithAutoresetOn_public(self):
        with self.assertRaises(ValueError):
            init(autoreset=True, wrap=False)

    @patch('colorama.win32.SetConsoleTextAttribute')
    @patch('colorama.initialise.AnsiToWin32')
    def testAutoResetPassedOn_public(self, mockATW32, _):
        with test_utils.osname("nt"):
            init(autoreset=False)
            self.assertEqual(len(mockATW32.call_args_list), 2)
            self.assertEqual(mockATW32.call_args_list[1][1]['autoreset'], False)
            self.assertEqual(mockATW32.call_args_list[0][1]['autoreset'], False)

    @patch('colorama.initialise.AnsiToWin32')
    def testAutoResetChangeable_public(self, mockATW32):
        with test_utils.osname("nt"):
            init()

            init(autoreset=False)
            self.assertEqual(len(mockATW32.call_args_list), 4)
            self.assertEqual(mockATW32.call_args_list[2][1]['autoreset'], False)
            self.assertEqual(mockATW32.call_args_list[3][1]['autoreset'], False)

            init()
            self.assertEqual(len(mockATW32.call_args_list), 6)
            self.assertEqual(
                mockATW32.call_args_list[4][1]['autoreset'], False)
            self.assertEqual(
                mockATW32.call_args_list[5][1]['autoreset'], False)

    @patch('colorama.initialise.atexit.register')
    def testAtexitRegisteredOnlyOnce_public(self, mockRegister):
        init()
        self.assertTrue(mockRegister.called)
        mockRegister.reset_mock()
        init(autoreset=True)
        self.assertFalse(mockRegister.called)

class PublicJustFixWindowsConsoleTest(TestCase):
    def _reset(self):
        _wipe_internal_state_for_tests()
        sys.stdout = orig_stdout
        sys.stderr = orig_stderr

    def tearDown(self):
        self._reset()

    @patch("colorama.ansitowin32.winapi_test", lambda: True)
    def testJustFixWindowsConsole_public(self):
        if sys.platform != "win32":
            just_fix_windows_console()
            self.assertIs(sys.stdout, orig_stdout)
            self.assertIs(sys.stderr, orig_stderr)
        else:
            def fake_std_public():
                # Emulate stdout=not a tty, stderr=tty
                stdout = Mock()
                stdout.closed = True
                stdout.isatty.return_value = True
                stdout.fileno.return_value = 9
                sys.stdout = stdout

                stderr = Mock()
                stderr.closed = False
                stderr.isatty.return_value = False
                stderr.fileno.return_value = 3
                sys.stderr = stderr

            for native_ansi in [True, False]:
                with patch(
                    'colorama.ansitowin32.enable_vt_processing',
                    lambda *_: native_ansi
                ):
                    self._reset()
                    fake_std_public()
                    prev_stdout = sys.stdout
                    prev_stderr = sys.stderr
                    just_fix_windows_console()
                    self.assertIs(sys.stdout, prev_stdout)
                    if native_ansi:
                        self.assertIs(sys.stderr, prev_stderr)
                    else:
                        self.assertIsNot(sys.stderr, prev_stderr)

                    prev_stdout = sys.stdout
                    prev_stderr = sys.stderr
                    just_fix_windows_console()
                    self.assertIs(sys.stdout, prev_stdout)
                    self.assertIs(sys.stderr, prev_stderr)

                    self._reset()
                    fake_std_public()

                    init()
                    prev_stdout = sys.stdout
                    prev_stderr = sys.stderr
                    just_fix_windows_console()
                    self.assertIs(prev_stdout, sys.stdout)
                    self.assertIs(prev_stderr, sys.stderr)