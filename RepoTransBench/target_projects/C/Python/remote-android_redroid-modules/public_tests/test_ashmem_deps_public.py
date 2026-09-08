import unittest
from src.ashmem.deps import VMAreaStruct, shmem_zero_setup, kallsyms_lookup_name

class TestAshmemDepsPublic(unittest.TestCase):
    def setUp(self):
        # Reset the global pointer between tests
        import src.ashmem.deps
        src.ashmem.deps.shmem_zero_setup_ptr = None
        
        # Define our public mock function - different return value from original
        def mock_shmem_zero_setup_public(vma):
            return 2024
        
        # Override the global kallsyms_lookup_name to return our public mock
        def mock_kallsyms_lookup_public(name):
            if name == "shmem_zero_setup":
                return mock_shmem_zero_setup_public
            return None
        
        # Store original function to restore later
        self.original_lookup = src.ashmem.deps.kallsyms_lookup_name
        # Replace with our public mock
        src.ashmem.deps.kallsyms_lookup_name = mock_kallsyms_lookup_public

    def tearDown(self):
        # Restore original function
        import src.ashmem.deps
        src.ashmem.deps.kallsyms_lookup_name = self.original_lookup
        src.ashmem.deps.shmem_zero_setup_ptr = None

    def test_shmem_zero_setup_public(self):
        """Public test for shmem_zero_setup with different mock."""
        # Create vma with specific values as in the C public test
        vma = VMAreaStruct(dummy=123, other=999)
        
        # First call should initialize the static pointer
        result1 = shmem_zero_setup(vma)
        
        # Second call should use the cached pointer
        result2 = shmem_zero_setup(vma)
        
        # Both calls should return the public mock value (2024, not 42)
        self.assertEqual(result1, 2024, "First call should return 2024 in public test")
        self.assertEqual(result2, 2024, "Second call should return 2024 in public test")

if __name__ == '__main__':
    unittest.main()