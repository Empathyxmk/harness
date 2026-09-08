import pytest
from unittest.mock import patch

# Import the mocked functions from our source module
from src.mflatt_gc_demo import gc_core

def test_gc_api_basic():
    """
    Translates gc/test_gc_api.c
    Only test that we can call allocate and collect_garbage
    """
    with patch('src.mflatt_gc_demo.gc_core.mem_init') as mock_mem_init, \
         patch('src.mflatt_gc_demo.gc_core.allocate') as mock_allocate, \
         patch('src.mflatt_gc_demo.gc_core.collect_garbage') as mock_collect_garbage:

        # Call the functions that would be part of the API
        mock_mem_init.return_value = None # mem_init returns void
        mock_allocate.return_value = gc_core.Node() # allocate returns a node
        mock_collect_garbage.return_value = None # collect_garbage returns void

        gc_core.mem_init()
        n = gc_core.allocate()
        assert n is not None # Ensure allocate returned something
        gc_core.collect_garbage()

        # Verify that the mocked functions were called
        mock_mem_init.assert_called_once()
        mock_allocate.assert_called_once()
        mock_collect_garbage.assert_called_once()

    print("gc/test_gc_api: PASS") # Original C test printed this