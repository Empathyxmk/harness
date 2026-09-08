import pytest

# Inline minimal definitions for ChunkedParser, mirroring C's self-contained test files
# Note: The C public test file explicitly states it recognizes "6\r\nPublic" etc.
# The underlying parser logic, however, is identical to the original's dummy parser.
class ChunkedParser:
    STATE_SIZE = 0
    STATE_EXTENSION = 1
    STATE_DATA = 2
    STATE_DATA_CR = 3
    STATE_DATA_LF = 4
    STATE_END_CR = 5
    STATE_END_LF = 6
    STATE_TRAILER = 7
    STATE_TRAILER_CR = 8
    STATE_ERROR = 9

    def __init__(self):
        self.state = self.STATE_SIZE
        self.chunk_size = 0
        self.bytes_read = 0
        self.last_chunk = 0

    def execute(self, data: str):
        for c in data:
            if self.state == self.STATE_SIZE:
                if '0' <= c <= '9':
                    self.chunk_size = self.chunk_size * 16 + (ord(c) - ord('0'))
                elif c == '\r':
                    self.state = self.STATE_EXTENSION
                else:
                    self.state = self.STATE_ERROR
            elif self.state == self.STATE_EXTENSION:
                if c == '\n':
                    if self.chunk_size == 0:
                        self.state = self.STATE_END_CR
                        self.last_chunk = 1
                    else:
                        self.state = self.STATE_DATA
                else:
                    self.state = self.STATE_ERROR
            elif self.state == self.STATE_DATA:
                self.bytes_read += 1
                if self.bytes_read == self.chunk_size:
                    self.state = self.STATE_DATA_CR
            elif self.state == self.STATE_DATA_CR:
                if c == '\r':
                    self.state = self.STATE_DATA_LF
                else:
                    self.state = self.STATE_ERROR
            elif self.state == self.STATE_DATA_LF:
                if c == '\n':
                    self.state = self.STATE_SIZE
                    self.chunk_size = 0
                    self.bytes_read = 0
                else:
                    self.state = self.STATE_ERROR
            elif self.state == self.STATE_END_CR:
                if c == '\r':
                    self.state = self.STATE_END_LF
                else:
                    self.state = self.STATE_ERROR
            elif self.state == self.STATE_END_LF:
                if c == '\n':
                    # done
                    pass
                else:
                    self.state = self.STATE_ERROR
            else: # Catches any other unexpected state, similar to C's default
                self.state = self.STATE_ERROR

def test_simple_chunk_public():
    """Public test for a simple valid chunked transfer: '6\\r\\nPublic\\r\\n0\\r\\n\\r\\n'."""
    parser = ChunkedParser()
    input_str = "6\r\nPublic\r\n0\r\n\r\n"
    
    for i, char in enumerate(input_str):
        parser.execute(char)
        if parser.state == parser.STATE_ERROR:
            pytest.fail(f"Public simple chunk: error at pos {i}")
    
    assert parser.state == parser.STATE_END_LF, \
        f"Public simple chunk: wrong end state: {parser.state}"
    print("Public simple chunk test passed.")

def test_nonzero_second_chunk_public():
    """Public test for two chunks: '2\\r\\nhi\\r\\n3\\r\\nbye\\r\\n0\\r\\n\\r\\n'."""
    parser = ChunkedParser()
    input_str = "2\r\nhi\r\n3\r\nbye\r\n0\r\n\r\n"
    
    for i, char in enumerate(input_str):
        parser.execute(char)
        if parser.state == parser.STATE_ERROR:
            pytest.fail(f"Public two-chunks test: error at pos {i}")
            
    assert parser.state == parser.STATE_END_LF, \
        f"Public two-chunks: wrong end state: {parser.state}"
    print("Public two-chunks test passed.")

def test_invalid_chunk_public():
    """Public test for an invalid chunked transfer with non-hex digit: 'z\\r\\nFail\\r\\n0\\r\\n\\r\\n'."""
    parser = ChunkedParser()
    input_str = "z\r\nFail\r\n0\r\n\r\n" # 'z' is not a hex digit
    
    hit_error = False
    for char in input_str:
        parser.execute(char)
        if parser.state == parser.STATE_ERROR:
            hit_error = True
            break # Expected to hit error early
            
    assert hit_error, "Public invalid input did not cause error!"
    print("Public invalid chunk test passed as expected (error detected).")