import unittest
from unittest.mock import MagicMock, patch

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
        # Mimics default Android behavior: returns False
        return False

    def onBackPressed(self):
        if self.circleMenu:
            self.circleMenu.closeMenu()


class TestMainActivity(unittest.TestCase):
    def setUp(self):
        self.main_activity = MainActivity()
        self.mock_circle_menu = MagicMock(spec=FakeCircleMenu)
        self.main_activity.circleMenu = self.mock_circle_menu

    def test_onMenuOpened_callsCircleMenuOpenMenu(self):
        mock_menu = MagicMock()
        self.mock_circle_menu.openMenu.return_value = None
        result = self.main_activity.onMenuOpened(1, mock_menu)
        self.mock_circle_menu.openMenu.assert_called_once()

    def test_onBackPressed_callsCircleMenuCloseMenu(self):
        self.main_activity.onBackPressed()
        self.mock_circle_menu.closeMenu.assert_called_once()