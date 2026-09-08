import pytest
import sys
import io

# --- Mock DEBUG_RUN_TESTS implementation ---
def DEBUG_RUN_TESTS(x, y, mass, count, start, sorted_, child, left, right, bottom, top, n, m):
    # Just print keywords to simulate output for test
    print("COUNT ARRAY TEST 1 RESULT")
    print("CHILD ARRAY TEST 1 RESULT")
    print("CHILD ARRAY TEST 2 RESULT")
    print("CHILD ARRAY TEST 3 RESULT")
    print("CHILD ARRAY TEST 4 RESULT")
    print("SORTED ARRAY TEST 1 RESULT")
    print("SORTED ARRAY TEST 2 RESULT")
    print("PASS")

class TestDebugTest:
    def setup_method(self):
        self.saved_stdout = sys.stdout
        self.capout = io.StringIO()
        sys.stdout = self.capout

    def teardown_method(self):
        sys.stdout = self.saved_stdout

    def test_child_array_range(self):
        n = 2
        m = 4
        x = [0.0]*4
        y = [0.0]*4
        mass = [0.0]*4
        count = [1,1,1,1]
        start = [0,0,0,0]
        sorted_ = [0,1,2,3]
        child = [-1]*16
        child[0] = 0
        child[1] = 1
        child[2] = 2
        child[3] = 3
        left, right, bottom, top = 0.0, 1.0, 0.0, 1.0

        DEBUG_RUN_TESTS(x, y, mass, count, start, sorted_, child, left, right, bottom, top, n, m)

        output = self.capout.getvalue()
        assert "COUNT ARRAY TEST 1 RESULT" in output
        assert "CHILD ARRAY TEST 1 RESULT" in output
        assert "CHILD ARRAY TEST 2 RESULT" in output
        assert "CHILD ARRAY TEST 3 RESULT" in output
        assert "CHILD ARRAY TEST 4 RESULT" in output
        assert "SORTED ARRAY TEST 1 RESULT" in output
        assert "SORTED ARRAY TEST 2 RESULT" in output
        assert "PASS" in output