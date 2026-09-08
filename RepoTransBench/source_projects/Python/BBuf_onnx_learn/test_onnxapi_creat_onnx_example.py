import unittest
from onnxapi.creat_onnx_example import make_identity, sum_list

class TestOnnxApiCreatOnnxExample(unittest.TestCase):

    def test_make_identity(self):
        self.assertEqual(make_identity(100), 100)
        self.assertEqual(make_identity([1,2,3]), [1,2,3])

    def test_sum_list(self):
        self.assertEqual(sum_list([1,2,3]), 6)
        self.assertEqual(sum_list([]), 0)

if __name__ == "__main__":
    unittest.main()