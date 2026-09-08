import unittest

class SubMenu:
    def __init__(self, color, iconResId):
        self._color = color
        self._iconResId = iconResId

    def getColor(self):
        return self._color
    def getIconResId(self):
        return self._iconResId

class CircleMenu:
    def __init__(self, context, attrs):
        self._mainMenuColor = None
        self._mainMenuIconNormal = None
        self._mainMenuIconPressed = None
        self._subMenus = []

    def setMainMenu(self, color, iconNormal, iconPressed):
        self._mainMenuColor = color
        self._mainMenuIconNormal = iconNormal
        self._mainMenuIconPressed = iconPressed

    def getMainMenuColor(self):
        return self._mainMenuColor

    def addSubMenu(self, color, iconResId):
        self._subMenus.append(SubMenu(color, iconResId))

    def getSubMenus(self):
        return self._subMenus

class TestCircleMenuPublic(unittest.TestCase):
    def setUp(self):
        self.circleMenu = CircleMenu(None, None)

    def test_setMainMenu_differentColor(self):
        self.circleMenu.setMainMenu(0xFF00FF00, 200, 201)
        self.assertEqual(0xFF00FF00, self.circleMenu.getMainMenuColor())

    def test_addSubMenu_differentIcons(self):
        self.circleMenu.addSubMenu(0xFFFF0000, 300)
        self.assertEqual(1, len(self.circleMenu.getSubMenus()))
        self.assertEqual(0xFFFF0000, self.circleMenu.getSubMenus()[0].getColor())
        self.assertEqual(300, self.circleMenu.getSubMenus()[0].getIconResId())