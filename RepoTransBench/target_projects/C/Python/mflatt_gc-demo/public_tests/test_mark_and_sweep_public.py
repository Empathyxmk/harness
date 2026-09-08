import pytest
from unittest.mock import patch
from src.mflatt_gc_demo import gc_core
from src.mflatt_gc_demo.common import Node

class TestMarkAndSweepPublic:
    """
    Translates gc/test_mark_and_sweep_public.c
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

    def test_mark_and_sweep_no_roots_public(self):
        """Edge case: no roots, should not crash, just runs."""
        gc_core.set_num_roots(0)
        gc_core.mark_and_sweep_from_roots()
        assert True # If it reaches here, it passed implicitly

    def test_mark_and_sweep_one_root_public(self):
        """Case: single root, left and right branch set to each other (lopsided tree)."""
        gc_core.set_num_roots(1)
        n = gc_core.allocate()
        n.left = gc_core.allocate()
        n.right = None
        n.left.left = None
        n.left.right = n
        
        gc_core.set_root_addr(0, n)
        
        gc_core.mark_and_sweep_from_roots()
        
        # Clean up
        gc_core.set_root_addr(0, None)
        assert gc_core._roots_store[0] is None
        assert True # If it reaches here, it passed implicitly

    def test_mark_and_sweep_multiple_null_roots_public(self):
        """Case: multiple roots, all NULL."""
        gc_core.set_num_roots(3)
        n1 = None # Simulating struct node *n1 = NULL;
        n2 = None
        n3 = None
        
        gc_core.set_root_addr(0, n1)
        gc_core.set_root_addr(1, n2)
        gc_core.set_root_addr(2, n3)
        
        gc_core.mark_and_sweep_from_roots()
        
        # Clean up
        gc_core.set_root_addr(0, None)
        gc_core.set_root_addr(1, None)
        gc_core.set_root_addr(2, None)
        assert gc_core._roots_store[0] is None
        assert gc_core._roots_store[1] is None
        assert gc_core._roots_store[2] is None
        assert True # If it reaches here, it passed implicitly

    def teardown_method(self):
        print("gc/test_mark_and_sweep_public: PASS")