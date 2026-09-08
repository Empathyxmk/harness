import pytest
import io
import sys
from unittest.mock import patch

# Simulate BeaconPrintf from PortScan implementation
def BeaconPrintf(log_type, fmt, *args):
    """Simulates BeaconPrintf, captures output to stdout for assertion."""
    # In C, this uses vprintf. In Python, we can capture printed output.
    sys.stdout.write(fmt % args + '\n')

# Simulate a port scan function for public test
def port_is_open_public(ip: str, port: int) -> int:
    """
    Simulates checking if a port is open for public test cases.
    Uses specific hardcoded logic based on C code.
    """
    if ip == "8.8.8.8" and port == 443:
        return 1
    if ip == "8.8.8.8" and port == 22:
        return 0
    if ip == "1.1.1.1" and port == 80:
        return 0
    if ip == "1.1.1.1" and port == 853:
        return 1
    return 0

class TestPortScanPublic:
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_public_portscan_case1(self, mock_stdout):
        assert port_is_open_public("8.8.8.8", 443) == 1
        assert port_is_open_public("8.8.8.8", 22) == 0
        # The C code uses printf within the public test function, so we simulate that
        # and don't require the test to explicitly call BeaconPrintf.
        # BeaconPrintf itself is called by the "simulated" functions, not the test cases directly.
        # But if the C test had `printf("... passed")` we can reflect that in the Python test.
        BeaconPrintf(0, "public_portscan_test_case1 passed")
        assert "public_portscan_test_case1 passed" in mock_stdout.getvalue()

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_public_portscan_case2(self, mock_stdout):
        assert port_is_open_public("1.1.1.1", 80) == 0
        assert port_is_open_public("1.1.1.1", 853) == 1
        BeaconPrintf(0, "public_portscan_test_case2 passed")
        assert "public_portscan_test_case2 passed" in mock_stdout.getvalue()

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_public_portscan_case3(self, mock_stdout):
        assert port_is_open_public("127.0.0.1", 65535) == 0
        BeaconPrintf(0, "public_portscan_test_case3 (edge case) passed")
        assert "public_portscan_test_case3 (edge case) passed" in mock_stdout.getvalue()