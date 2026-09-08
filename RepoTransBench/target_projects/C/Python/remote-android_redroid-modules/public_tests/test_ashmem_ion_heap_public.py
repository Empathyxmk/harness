import unittest
from src.binder.binder_alloc import vmap, vunmap

class TestAshmemIonHeapPublic(unittest.TestCase):
    def test_vmap_vunmap_public(self):
        """Public test for vmap/vunmap with different page count."""
        # Public test: map+unmap 2 pages (vs 1 in original)
        v = vmap(None, 2, 0, 0)
        self.assertIsNotNone(v, "vmap should return a non-null pointer")
        # In this public test, we allocated 2 pages instead of 1
        self.assertEqual(len(v), 4096 * 2, "vmap should allocate 2 * PAGE_SIZE bytes")
        
        vunmap(v)
        # No assertion needed for vunmap since it doesn't return anything

if __name__ == '__main__':
    unittest.main()