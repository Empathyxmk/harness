import unittest
from unittest.mock import patch, Mock
from colorama.winterm import WinTerm

class PublicWinTermTest(unittest.TestCase):
    @patch('colorama.winterm.win32')
    def testInit_public(self, mockWin32):
        mockAttr = Mock()
        # The colorama WinTerm expects:
        # _fore = wAttributes & 7
        # _back = (wAttributes >> 4) & 7
        # _style = wAttributes & ~0x77
        # Let's choose wAttributes = 171: 0b10101011
        # _fore = 171 & 7 = 3
        # _back = (171 >> 4) & 7 = (10) & 7 = 2
        # _style = 171 & ~0x77 = 171 & 0x88 = 0x88 = 136
        mockAttr.wAttributes = 171
        mockWin32.GetConsoleScreenBufferInfo.return_value = mockAttr
        term = WinTerm()
        self.assertEqual(term._fore, 3)
        self.assertEqual(term._back, 2)
        self.assertEqual(term._style, 136)

    @patch('colorama.winterm.win32')
    def testResetAll_public(self, mockWin32):
        mockAttr = Mock()
        # wAttributes = 250: 0b11111010
        # _fore = 250 & 7 = 2
        # _back = (250 >> 4) & 7 = (15) & 7 = 7
        # _style = 250 & ~0x77 = 250 & 0x88 = 136
        mockAttr.wAttributes = 250
        mockWin32.GetConsoleScreenBufferInfo.return_value = mockAttr
        term = WinTerm()

        term.set_console = Mock()
        # Mess up internal state
        term._fore = 1
        term._back = 3
        term._style = 0

        term.reset_all()
        self.assertEqual(term._fore, 2)
        self.assertEqual(term._back, 7)
        self.assertEqual(term._style, 136)