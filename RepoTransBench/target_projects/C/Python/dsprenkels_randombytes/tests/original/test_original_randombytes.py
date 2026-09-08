# tests/original/test_original_randombytes.py
import pytest
from src.randombytes_mod import randombytes

def test_functional():
    """
    Corresponds to C's `test_functional`.
    Tests if two calls to randombytes yield different results.
    """
    buf1 = bytearray(20)
    buf2 = bytearray(20)

    ret1 = randombytes(buf1, len(buf1))
    ret2 = randombytes(buf2, len(buf2))

    assert ret1 == 0
    assert ret2 == 0
    assert buf1 != buf2, "Buffers should contain different random data"

def test_empty():
    """
    Corresponds to C's `test_empty`.
    Tests calling randombytes with a length of 0.
    """
    zero_buf = bytearray(20) # A reference buffer filled with zeros
    buf = bytearray(20)      # Buffer to be passed to randombytes

    # Ensure buffer is initially zeroed (similar to C's static init)
    for i in range(len(buf)):
        buf[i] = 0

    ret = randombytes(buf, 0)
    assert ret == 0
    assert buf == zero_buf, "Buffer should remain unchanged when n=0"

def test_getrandom_partial(mock_getrandom_partial):
    """
    Corresponds to C's `test_getrandom_syscall_partial` and `test_getrandom_glib_partial`.
    Tests `randombytes`'s ability to handle partial reads from the underlying source.
    """
    buf = bytearray(100)
    ret = randombytes(buf, len(buf))
    assert ret == 0
    # The randombytes function should have retried and filled the entire buffer.
    # We check that different 20-byte chunks are indeed different, implying
    # successful filling with random data.
    for i in range(1, 5): # Check chunks at 0, 20, 40, 60, 80 offsets
        assert buf[0:20] != buf[20*i:20*i+20], "Chunks should be different, indicating proper random fill"

def test_getrandom_interrupted(mock_getrandom_interrupted):
    """
    Corresponds to C's `test_getrandom_syscall_interrupted` and `test_getrandom_glib_interrupted`.
    Tests `randombytes`'s ability to handle `EINTR` (interrupted calls) by retrying.
    """
    zero_buf = bytearray(20) # Reference buffer filled with zeros
    buf = bytearray(20)      # Buffer to be filled

    # Ensure buffer is initially zeroed
    for i in range(len(buf)):
        buf[i] = 0

    ret = randombytes(buf, len(buf))
    assert ret == 0
    # The buffer should be filled with random data despite interruptions.
    assert buf != zero_buf, "Buffer should be filled with random data despite simulated interruptions"


# The following tests (`test_issue_17`, `test_issue_22`, `test_issue_33`) are
# platform-specific in the C source (`__linux__ && !SYS_getrandom`).
# They involve mocking `ioctl` calls, which are low-level system interactions
# not directly exposed or relevant for `os.urandom` (Python's typical random source).
# Without the specific C implementation of `randombytes.c`, replicating the exact
# fallback logic and `ioctl` errors is not feasible or necessary for `os.urandom` based
# Python `randombytes` as it handles system randomness differently.
# Therefore, these tests are marked as skipped to reflect their conditional nature
# and the difference in underlying OS interaction.

@pytest.mark.skip(reason="C test logic for Linux-specific ioctl fallback (issue #17) is not directly translatable to Python's os.urandom context.")
def test_issue_17():
    pass

@pytest.mark.skip(reason="C test logic for Linux-specific ioctl fallback (issue #22) is not directly translatable to Python's os.urandom context.")
def test_issue_22():
    pass

@pytest.mark.skip(reason="C test logic for Linux-specific ioctl fallback (issue #33 stress test) is not directly translatable to Python's os.urandom context.")
def test_issue_33():
    pass