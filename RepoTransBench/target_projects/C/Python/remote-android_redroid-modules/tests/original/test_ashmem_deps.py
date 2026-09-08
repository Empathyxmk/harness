import unittest
from src.ashmem.deps import VMAreaStruct, shmem_zero_setup, kallsyms_lookup_name

class TestAshmemDeps(unittest.TestCase):
    def setUp(self):
        # Reset the global pointer between tests
        import src.ashmem.deps
        src.ashmem.deps.shmem_zero_setup_ptr = None
        
        # Define our mock function
        def mock_shmem_zero_setup(vma):
            return 42
        
        # Override the global kallsyms_lookup_name to return our mock
        def mock_kallsyms_lookup(name):
            if name == "shmem_zero_setup":
                return mock_shmem_zero_setup
            return None
        
        # Store original function to restore later
        self.original_lookup = src.ashmem.deps.kallsyms_lookup_name
        # Replace with our mock
        src.ashmem.deps.kallsyms_lookup_name = mock_kallsyms_lookup

    def tearDown(self):
        # Restore original function
        import src.ashmem.deps
        src.ashmem.deps.kallsyms_lookup_name = self.original_lookup
        src.ashmem.deps.shmem_zero_setup_ptr = None

    def test_shmem_zero_setup(self):
        """Test that shmem_zero_setup initializes and uses cached pointer."""
        vma = VMAreaStruct()
        
        # First call should initialize the static pointer
        result1 = shmem_zero_setup(vma)
        
        # Second call should use the cached pointer
        result2 = shmem_zero_setup(vma)
        
        # Both calls should return the same result from our mock (42)
        self.assertEqual(result1, 42, "First call to shmem_zero_setup should return 42")
        self.assertEqual(result2, 42, "Second call to shmem_zero_setup should return 42")
        
        # We could also test the NULL branch, but in the C code this would
        # cause a NULL dereference, and they skipped it for safety

if __name__ == '__main__':
    unittest.main()