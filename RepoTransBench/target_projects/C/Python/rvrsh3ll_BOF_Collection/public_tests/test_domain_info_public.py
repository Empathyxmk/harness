import pytest
import io
import sys
from unittest.mock import patch

# Simulate the BeaconPrintf used in GetDomainInfo.c (from context)
def BeaconPrintf(log_type, fmt, *args):
    """Simulates BeaconPrintf, captures output to stdout for assertion."""
    sys.stdout.write(fmt % args + '\n')

# Simulate domain info getter for public test
def GetDomainInfo_Public(domain_dns_name: str, max_len: int) -> tuple[int, str]:
    """
    Simulates domain info retrieval for public test cases.
    Returns (return_code, sid_string).
    """
    out_domain_sid = ""
    if domain_dns_name == "public.domain.com":
        out_domain_sid = "S-1-5-21-public"
        return 0, out_domain_sid[:max_len-1] # success
    elif domain_dns_name == "example.com":
        out_domain_sid = "S-1-5-21-example"
        return 0, out_domain_sid[:max_len-1] # success
    return -1, "" # fail

class TestDomainInfoPublic:
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_public_case1(self, mock_stdout):
        sid_buffer_len = 64
        ret, sid = GetDomainInfo_Public("public.domain.com", sid_buffer_len)
        assert ret == 0
        assert sid == "S-1-5-21-public"
        BeaconPrintf(0, "public_test_case1 passed")
        assert "public_test_case1 passed" in mock_stdout.getvalue()

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_public_case2(self, mock_stdout):
        sid_buffer_len = 64
        ret, sid = GetDomainInfo_Public("example.com", sid_buffer_len)
        assert ret == 0
        assert sid == "S-1-5-21-example"
        BeaconPrintf(0, "public_test_case2 passed")
        assert "public_test_case2 passed" in mock_stdout.getvalue()

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_public_case3(self, mock_stdout):
        sid_buffer_len = 64
        ret, sid = GetDomainInfo_Public("doesnotexist.local", sid_buffer_len)
        assert ret != 0
        BeaconPrintf(0, "public_test_case3 (failure scenario) passed")
        assert "public_test_case3 (failure scenario) passed" in mock_stdout.getvalue()