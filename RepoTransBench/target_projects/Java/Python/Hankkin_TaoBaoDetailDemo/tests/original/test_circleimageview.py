import unittest

class MockImageView:
    # Simulates only the parts tested
    class ScaleType:
        CENTER_CROP = "CENTER_CROP"
        FIT_XY = "FIT_XY"

    def __init__(self):
        self._scale_type = self.ScaleType.CENTER_CROP
        self._adjust_view_bounds = False

    def getScaleType(self):
        return self._scale_type

    def setScaleType(self, scale_type):
        if scale_type != self.ScaleType.CENTER_CROP:
            raise ValueError("Only CENTER_CROP is supported!")
        self._scale_type = scale_type

    def setAdjustViewBounds(self, adjust):
        if adjust:
            raise ValueError("Circular image view does not support adjustViewBounds!")
        self._adjust_view_bounds = adjust

class CircleImageView(MockImageView):
    def __init__(self, context, attrs=None):
        super().__init__()
        self.border_color = 0
        self.border_width = 0
        self.fill_color = 0
        self.circular_transformation_disabled = False

    def setBorderColor(self, color):
        self.border_color = color

    def getBorderColor(self):
        return self.border_color

    def setBorderWidth(self, width):
        self.border_width = width

    def getBorderWidth(self):
        return self.border_width

    def setFillColor(self, color):
        self.fill_color = color

    def getFillColor(self):
        return self.fill_color

    def setDisableCircularTransformation(self, disabled):
        self.circular_transformation_disabled = disabled

    def isDisableCircularTransformation(self):
        return self.circular_transformation_disabled

    def onDraw(self, canvas):
        # Do nothing if no bitmap set (simulating original test)
        pass

class TestCircleImageView(unittest.TestCase):

    def setUp(self):
        self.context = object()  # Dummy context

    def test_constructors_and_init(self):
        civ1 = CircleImageView(self.context)
        self.assertEqual(MockImageView.ScaleType.CENTER_CROP, civ1.getScaleType())

        civ2 = CircleImageView(self.context, attrs={})
        self.assertEqual(MockImageView.ScaleType.CENTER_CROP, civ2.getScaleType())

    def test_set_scale_type_throws(self):
        civ = CircleImageView(self.context)
        with self.assertRaises(ValueError):
            civ.setScaleType(MockImageView.ScaleType.FIT_XY)

    def test_set_adjust_view_bounds_throws(self):
        civ = CircleImageView(self.context)
        with self.assertRaises(ValueError):
            civ.setAdjustViewBounds(True)

    def test_on_draw_with_no_bitmap(self):
        civ = CircleImageView(self.context)
        try:
            civ.onDraw(None)
        except Exception as e:
            self.fail(f"onDraw raised an exception: {e}")

    def test_set_border_and_fill_color(self):
        civ = CircleImageView(self.context)
        civ.setBorderColor(0x0000FF)  # Blue
        civ.setBorderWidth(5)
        civ.setFillColor(0xFFFF00)  # Yellow
        self.assertEqual(0x0000FF, civ.getBorderColor())
        self.assertEqual(5, civ.getBorderWidth())
        self.assertEqual(0xFFFF00, civ.getFillColor())

    def test_set_disable_circular_transformation(self):
        civ = CircleImageView(self.context)
        civ.setDisableCircularTransformation(True)
        self.assertTrue(civ.isDisableCircularTransformation())
        civ.setDisableCircularTransformation(False)
        self.assertFalse(civ.isDisableCircularTransformation())