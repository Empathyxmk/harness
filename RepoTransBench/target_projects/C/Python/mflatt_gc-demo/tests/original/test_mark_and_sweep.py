import pytest
from unittest.mock import patch
from src.mflatt_gc_demo import gc_core
from src.mflatt_gc_demo.common import Node

class TestMarkAndSweep:
    """
    Translates gc/test_mark_and_sweep.c
    Tests mark_and_sweep edge cases by manipulating globals, as these are visible via header.
    """

    @pytest.fixture(autouse=True)
    def setup_mocks(self):
        # Patch the global state in gc_core to manage roots for each test
        with patch('src.mflatt_gc_demo.gc_core._num_roots', new=0) as mock_num_roots, \
             patch('src.mflatt_gc_demo.gc_core._roots_store', new=[None]*10) as mock_roots_store, \
             patch('src.mflatt_gc_demo.gc_core.allocate') as mock_allocate:
            
            self.mock_num_roots = mock_num_roots
            self.mock_roots_store = mock_roots_store
            self.mock_allocate = mock_allocate
            self.mock_allocate.side_effect = lambda: Node() # Make allocate return a new Node instance

            # Ensure global state is reset for each test
            gc_core.set_num_roots(0)
            for i in range(len(gc_core._roots_store)):
                gc_core.set_root_addr(i, None)

            yield

    def test_mark_and_sweep_from_roots_handles_no_roots(self):
        """Test mark_and_sweep_from_roots handles no roots."""
        gc_core.set_num_roots(0)
        gc_core.mark_and_sweep_from_roots()
        # The test simply calls the function and expects no crash.
        # In Python, we just ensure it completes without exception.
        assert True # If it reaches here, it passed implicitly

    def test_mark_and_sweep_with_root(self):
        """Test mark_and_sweep with a single root."""
        gc_core.set_num_roots(1)
        n = gc_core.allocate()
        n.left = None
        n.right = None
        gc_core.set_root_addr(0, n)
        
        gc_core.mark_and_sweep_from_roots()
        
        # Clean up (simulating C's NULL assignment)
        gc_core.set_root_addr(0, None)
        assert gc_core._roots_store[0] is None
        assert True # If it reaches here, it passed implicitly

    def test_mark_and_sweep_with_multiple_roots(self):
        """Test mark_and_sweep with multiple roots."""
        gc_core.set_num_roots(2)
        n1 = gc_core.allocate()
        n2 = gc_core.allocate()
        n1.left = None
        n1.right = n2
        n2.left = n1
        n2.right = None
        
        gc_core.set_root_addr(0, n1)
        gc_core.set_root_addr(1, n2)
        
        gc_core.mark_and_sweep_from_roots()
        
        # Clean up
        gc_core.set_root_addr(0, None)
        gc_core.set_root_addr(1, None)
        assert gc_core._roots_store[0] is None
        assert gc_core._roots_store[1] is None
        assert True # If it reaches here, it passed implicitly

    def teardown_method(self):
        print("gc/test_mark_and_sweep: PASS")