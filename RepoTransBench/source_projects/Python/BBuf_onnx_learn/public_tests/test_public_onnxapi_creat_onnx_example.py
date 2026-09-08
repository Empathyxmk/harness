import unittest
from onnxapi.creat_onnx_example import make_identity, sum_list

class TestPublicOnnxApiCreatOnnxExample(unittest.TestCase):

    def test_make_identity(self):
        self.assertEqual(make_identity("hello"), "hello")
        self.assertEqual(make_identity([7,8,9]), [7,8,9])

    def test_sum_list(self):
        self.assertEqual(sum_list([4,5,6]), 15)
        self.assertEqual(sum_list([100]), 100)

if __name__ == "__main__":
    unittest.main()