import unittest
from src.binder.binder_alloc import vmap, vunmap

class TestAshmemIonHeap(unittest.TestCase):
    def test_vmap_vunmap(self):
        """Test the vmap and vunmap functions."""
        # Simple test: map+unmap kernel simulation
        v = vmap(None, 1, 0, 0)
        self.assertIsNotNone(v, "vmap should return a non-null pointer")
        self.assertEqual(len(v), 4096, "vmap should allocate PAGE_SIZE bytes")
        
        # In C they'd check for NULL, but in Python we just check it's not None
        vunmap(v)
        # No assertion needed for vunmap since it doesn't return anything
        # In C, we'd check for memory leaks, but Python handles that for us

if __name__ == '__main__':
    unittest.main()