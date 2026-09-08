import unittest
from src.fastrange import fastrange64, UINT32_MAX, UINT64_MAX

class TestFastRangeExtra(unittest.TestCase):
    def test_typical(self):
        # typical cases from test_fastrange_extra.c
        self.assertLess(fastrange64(1234567890123, 1000), 1000)
        self.assertEqual(fastrange64(0, 42), 0)
        self.assertEqual(fastrange64(1, 10), 0)
        
    def test_edge_values(self):
        # edge values from test_fastrange_extra.c
        self.assertLess(fastrange64(UINT64_MAX, UINT32_MAX), UINT32_MAX)
        self.assertLessEqual(fastrange64(UINT64_MAX, UINT64_MAX), UINT64_MAX)
        self.assertEqual(fastrange64(0, UINT64_MAX), 0)

if __name__ == '__main__':
    unittest.main()