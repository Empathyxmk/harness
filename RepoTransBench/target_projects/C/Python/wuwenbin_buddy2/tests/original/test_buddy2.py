import unittest
from src.buddy2 import buddy2_new, buddy2_destroy, buddy2_alloc, buddy2_free, buddy2_size, buddy2_dump

class TestBuddy2(unittest.TestCase):
    
    def test_buddy2_new_destroy(self):
        # Test invalid size (<1)
        b = buddy2_new(0)
        self.assertIsNone(b)

        # Test invalid size (not power of 2)
        b = buddy2_new(30)
        self.assertIsNone(b)

        # Correct size
        b = buddy2_new(16)
        self.assertIsNotNone(b)
        buddy2_destroy(b)
    
    def test_buddy2_alloc_basic(self):
        b = buddy2_new(8)
        self.assertIsNotNone(b)

        # Should fully allocate
        o1 = buddy2_alloc(b, 1)
        self.assertGreaterEqual(o1, 0)
        o2 = buddy2_alloc(b, 2)
        self.assertGreaterEqual(o2, 0)
        o3 = buddy2_alloc(b, 3)  # Not power of 2, should round to 4
        self.assertGreaterEqual(o3, 0)
        o4 = buddy2_alloc(b, 2)
        # Only 1 block left, 2 is too big, should fail
        self.assertEqual(o4, -1)

        buddy2_destroy(b)
    
    def test_buddy2_alloc_edge_cases(self):
        b = buddy2_new(4)
        self.assertIsNotNone(b)

        # Allocate with size 0 (should become 1)
        o = buddy2_alloc(b, 0)
        self.assertGreaterEqual(o, 0)

        # Try to allocate more than available
        o2 = buddy2_alloc(b, 8)
        self.assertEqual(o2, -1)

        # Try NULL pointer
        self.assertEqual(buddy2_alloc(None, 2), -1)

        buddy2_destroy(b)
    
    def test_buddy2_free_and_size(self):
        b = buddy2_new(8)
        self.assertIsNotNone(b)

        o1 = buddy2_alloc(b, 4)
        o2 = buddy2_alloc(b, 2)
        o3 = buddy2_alloc(b, 1)

        # Free second alloc and check re-allocation
        buddy2_free(b, o2)

        o4 = buddy2_alloc(b, 2)
        self.assertEqual(o4, o2)  # Should get the same spot

        # Buddy2_size for allocated block
        sz = buddy2_size(b, o1)
        self.assertEqual(sz, 4)

        # Buddy2_size for smallest block
        sz = buddy2_size(b, o3)
        self.assertEqual(sz, 1)

        buddy2_destroy(b)
    
    def test_buddy2_alloc_free_full_cycle(self):
        b = buddy2_new(4)
        self.assertIsNotNone(b)

        # Fully allocate and free all, check all state resets
        o1 = buddy2_alloc(b, 2)
        o2 = buddy2_alloc(b, 2)

        # All memory should be used up
        self.assertEqual(buddy2_alloc(b, 1), -1)

        # Free both, try again
        buddy2_free(b, o1)
        buddy2_free(b, o2)

        o3 = buddy2_alloc(b, 4)  # Should get entire block
        self.assertGreaterEqual(o3, 0)

        buddy2_destroy(b)
    
    def test_buddy2_dump(self):
        b = buddy2_new(8)
        self.assertIsNotNone(b)

        # Simple smoke test (just to touch code, output not validated)
        buddy2_dump(None)  # triggers NULL handling
        buddy2_dump(b)

        # Oversize check
        large = buddy2_new(128)
        buddy2_dump(large)

        buddy2_destroy(large)
        buddy2_destroy(b)

if __name__ == '__main__':
    unittest.main()