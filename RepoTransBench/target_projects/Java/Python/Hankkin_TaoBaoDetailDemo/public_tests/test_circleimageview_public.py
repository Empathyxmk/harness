import unittest

class CircleImageView:
    def __init__(self, context):
        self.border_color = 0
        self.border_width = 0
        self.fill_color = 0
        self._border_overlay = False

    def setBorderColor(self, c):
        self.border_color = c

    def getBorderColor(self):
        return self.border_color

    def setBorderWidth(self, w):
        self.border_width = w

    def getBorderWidth(self):
        return self.border_width

    def setFillColor(self, c):
        self.fill_color = c

    def getFillColor(self):
        return self.fill_color

    def setBorderOverlay(self, v):
        self._border_overlay = v

    def isBorderOverlay(self):
        return self._border_overlay

class TestCircleImageViewPublic(unittest.TestCase):
    class MockContext:
        pass

    def test_border_color_change(self):
        context = self.MockContext()
        civ = CircleImageView(context)
        civ.setBorderColor(0xFF0000)  # 'Color.RED'
        self.assertEqual(0xFF0000, civ.getBorderColor())
        civ.setBorderColor(0x00FF00)  # 'Color.GREEN'
        self.assertEqual(0x00FF00, civ.getBorderColor())

    def test_border_width_change(self):
        context = self.MockContext()
        civ = CircleImageView(context)
        civ.setBorderWidth(8)
        self.assertEqual(8, civ.getBorderWidth())
        civ.setBorderWidth(0)
        self.assertEqual(0, civ.getBorderWidth())

    def test_fill_color_change(self):
        context = self.MockContext()
        civ = CircleImageView(context)
        civ.setFillColor(0xFFFF00)  # 'Color.YELLOW'
        self.assertEqual(0xFFFF00, civ.getFillColor())
        civ.setFillColor(0x00FFFF)  # 'Color.CYAN'
        self.assertEqual(0x00FFFF, civ.getFillColor())

    def test_border_overlay_change(self):
        context = self.MockContext()
        civ = CircleImageView(context)
        civ.setBorderOverlay(True)
        self.assertTrue(civ.isBorderOverlay())
        civ.setBorderOverlay(False)
        self.assertFalse(civ.isBorderOverlay())