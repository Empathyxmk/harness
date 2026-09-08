import unittest
from convert2onnx.pytorch2onnx_resize import dummy_resize_func

class TestPyTorch2ONNXResize(unittest.TestCase):

    def test_dummy_resize_func(self):
        self.assertEqual(dummy_resize_func(4, 5), (4, 5))
        self.assertEqual(dummy_resize_func('x', 42), ('x', 42))

if __name__ == "__main__":
    unittest.main()