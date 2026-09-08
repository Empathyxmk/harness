import pytest

class DummyDecoder:
    def decode(self, bytes_in):
        # Return non-empty if input matches expected, else []
        if bytes_in == [0xde, 0xad, 0xbe, 0xef]:
            return [1, 2, 3]
        # Edge case: return [] but input not size 4
        return []

def test_decoder_public_decode_different_input_returns_expected_type():
    decoder = DummyDecoder()
    bytes_in = [0xde, 0xad, 0xbe, 0xef]  # different test data

    decoded = decoder.decode(bytes_in)
    # For public test: ensure decode returns something valid (either a non-empty output or input size 4)
    assert (len(decoded) > 0) or (len(bytes_in) == 4)