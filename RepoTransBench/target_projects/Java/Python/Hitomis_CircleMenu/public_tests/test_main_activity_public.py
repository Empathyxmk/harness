import unittest
from unittest.mock import MagicMock

class FakeCircleMenu:
    def openMenu(self):
        pass
    def closeMenu(self):
        pass

class MainActivity:
    def __init__(self):
        self.circleMenu = None

    def onMenuOpened(self, featureId, menu):
        if self.circleMenu:
            self.circleMenu.openMenu()
        return False

    def onBackPressed(self):
        if self.circleMenu:
            self.circleMenu.closeMenu()

class TestMainActivityPublic(unittest.TestCase):
    def setUp(self):
        self.main_activity = MainActivity()
        self.mock_circle_menu = MagicMock(spec=FakeCircleMenu)
        self.main_activity.circleMenu = self.mock_circle_menu

    def test_onMenuOpened_callsOpenMenu_twice(self):
        mock_menu = MagicMock()
        self.mock_circle_menu.openMenu.return_value = None
        self.main_activity.onMenuOpened(2, mock_menu)
        self.main_activity.onMenuOpened(3, mock_menu)
        self.assertEqual(self.mock_circle_menu.openMenu.call_count, 2)

    def test_onBackPressed_callsCircleMenuCloseMenu_multipleTimes(self):
        self.main_activity.onBackPressed()
        self.main_activity.onBackPressed()
        self.assertEqual(self.mock_circle_menu.closeMenu.call_count, 2)