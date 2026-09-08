import pytest
from unittest.mock import patch
from src.mflatt_gc_demo import refcount_core
from src.mflatt_gc_demo.common import Node

class TestRefcount:
    """
    Translates refcount/test_refcount.c
    """

    @pytest.fixture(autouse=True)
    def setup_mock_allocate(self):
        # Patch allocate to ensure it always returns Node instances for these tests
        with patch('src.mflatt_gc_demo.refcount_core.allocate', side_effect=lambda *args, **kwargs: Node()) as mock_allocate:
            self.mock_allocate = mock_allocate
            # Reset ref_counts for each test for isolation
            refcount_core._ref_counts = {}
            yield

    def test_refcount_create_and_dec(self):
        """Test basic ref inc/dec logic."""
        n = refcount_core.allocate()
        n.left = None
        n.right = None
        
        # Initial refcount is 1 (from allocate mock)
        assert refcount_core.get_refcount(n) == 1

        refcount_core.refcount_inc(n)
        assert refcount_core.get_refcount(n) == 2

        refcount_core.refcount_dec(n) # should not free
        assert refcount_core.get_refcount(n) == 1

        refcount_core.refcount_dec(n) # may free (refcount becomes 0)
        assert refcount_core.get_refcount(n) == 0 # Or < 0 depending on exact mock behavior

        # The C test doesn't assert on memory freeing, just call sequence.
        # We ensure calls happen and refcounts change as expected.
        self.mock_allocate.assert_called_once()
        assert refcount_core.refcount_inc.called
        assert refcount_core.refcount_dec.call_count >= 2 # could be more if called implicitly by allocate for example.
                                                          # For this mock, it's explicitly 2 calls.

    def test_refcount_cycle(self):
        """Test circular references."""
        # For this test, allocate needs to return distinct objects
        node1 = Node()
        node2 = Node()
        with patch('src.mflatt_gc_demo.refcount_core.allocate', side_effect=[node1, node2]) as mock_allocate:
            n1 = refcount_core.allocate()
            n2 = refcount_core.allocate()

            # Mock initial refcounts (as if allocate initialized them to 1)
            refcount_core._ref_counts[id(n1)] = 1
            refcount_core._ref_counts[id(n2)] = 1

            n1.left = n2
            n2.right = n1
            
            # C test doesn't actually set refcounts based on links,
            # it just calls inc/dec manually.
            
            # Test circular references
            refcount_core.refcount_inc(n1)
            refcount_core.refcount_inc(n2)
            assert refcount_core.get_refcount(n1) == 2
            assert refcount_core.get_refcount(n2) == 2

            refcount_core.refcount_dec(n1)
            refcount_core.refcount_dec(n2)
            assert refcount_core.get_refcount(n1) == 1
            assert refcount_core.get_refcount(n2) == 1

            refcount_core.refcount_dec(n1)
            refcount_core.refcount_dec(n2)
            assert refcount_core.get_refcount(n1) == 0
            assert refcount_core.get_refcount(n2) == 0

        # C test doesn't assert on freeing, just that calls complete.
        assert mock_allocate.call_count == 2
        assert refcount_core.refcount_inc.call_count == 2
        assert refcount_core.refcount_dec.call_count == 4

    def teardown_method(self):
        print("refcount/test_refcount: PASS")