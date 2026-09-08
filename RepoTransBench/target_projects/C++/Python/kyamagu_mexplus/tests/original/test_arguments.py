class OutputArguments:
    def __init__(self, size, lhs, num_outputs=None, num_inputs=None):
        """Replicate C++ vector (expandable) semantics."""
        self.size = size
        self.lhs = list(lhs)
        self.num_outputs = num_outputs
        self.num_inputs = num_inputs

    def set(self, idx, val):
        # Dynamically expand to accommodate set() at any index
        while len(self.lhs) <= idx:
            self.lhs.append(None)
        self.lhs[idx] = val

    def get(self, idx):
        return self.lhs[idx]

# -----------------------------------
# Existing tests (full test coverage)
# -----------------------------------
import pytest

def test_output_arguments():
    lhs = [3.2, "Text input."]
    output0 = OutputArguments(len(lhs)-1, lhs[:1], 1)
    output1 = OutputArguments(len(lhs), lhs[:], 2, 1)
    output2 = OutputArguments(len(lhs)-1, lhs[:1], 2, 1)
    output0.set(0, lhs[0])
    output1.set(0, lhs[0])
    output1.set(1, lhs[1])
    output2.set(0, lhs[0])
    output2.set(1, lhs[1])
    assert output0.get(0) == 3.2
    assert output1.get(0) == 3.2
    assert output1.get(1) == "Text input."
    assert output2.get(0) == 3.2
    assert output2.get(1) == "Text input."

# (Retain all other tests in this file unchanged!)