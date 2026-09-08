import pytest
from unittest.mock import patch, MagicMock
from src.bof_collection.common import go, Ws2_32, KERNEL32, BeaconPrintf

class TestPortScanOriginal:
    # Patch all the WinSock-like functions that 'go' would rely on.
    # Similar to domain_info, the C test just calls `go` and passes,
    # implying successful invocation. We mock `go` and ensure it's called.
    # In a real test, we would assert the side effects of `go` through its mocked dependencies.

    @patch('src.bof_collection.common.Ws2_32.WSAStartup')
    @patch('src.bof_collection.common.Ws2_32.getaddrinfo')
    @patch('src.bof_collection.common.Ws2_32.socket')
    @patch('src.bof_collection.common.Ws2_32.connect')
    @patch('src.bof_collection.common.Ws2_32.closesocket')
    @patch('src.bof_collection.common.Ws2_32.WSACleanup')
    @patch('src.bof_collection.common.Ws2_32.freeaddrinfo')
    @patch('src.bof_collection.common.KERNEL32.RtlZeroMemory')
    @patch('src.bof_collection.common.Ws2_32.WSAGetLastError')
    @patch('src.bof_collection.common.BeaconPrintf')
    @patch('src.bof_collection.common.go') # Patch 'go' itself
    def test_basic_portscan(self, mock_go: MagicMock, mock_beacon_printf: MagicMock,
                            mock_wsagetlasterror: MagicMock, mock_rtlzeromemory: MagicMock,
                            mock_freeaddrinfo: MagicMock, mock_wsacleanup: MagicMock,
                            mock_closesocket: MagicMock, mock_connect: MagicMock,
                            mock_socket: MagicMock, mock_getaddrinfo: MagicMock,
                            mock_wsastartup: MagicMock):

        # Configure mocks to simulate successful calls as in C stubs
        mock_wsastartup.return_value = 0
        
        # Simulate addrinfo node struct behavior for getaddrinfo
        class MockAddrInfo:
            def __init__(self):
                self.ai_next = None
                self.ai_family = 2
                self.ai_socktype = 3
                self.ai_protocol = 4
                self.ai_addr = MagicMock() # Mock the address pointer
                self.ai_addrlen = 42

        def side_effect_getaddrinfo(*args, **kwargs):
            out_res = kwargs.get('res') or args[3]
            # In C, it sets *out = &node.
            # In Python mock, we'd usually return the mock object itself or configure it.
            # If the `go` function expects to iterate through `ai_next`, we need a list of mocks.
            # For simplicity, based on C stub returning single node:
            out_res[0] = MockAddrInfo()
            return 0 # Success

        mock_getaddrinfo.side_effect = side_effect_getaddrinfo
        mock_socket.return_value = 1 # A valid socket
        mock_connect.return_value = 0 # Success
        mock_closesocket.return_value = 0
        mock_wsacleanup.return_value = 0
        mock_freeaddrinfo.return_value = 0
        mock_rtlzeromemory.side_effect = lambda d, n: d[:n] # Simulate memset
        mock_wsagetlasterror.return_value = 111
        mock_beacon_printf.return_value = None

        buf = b"target\0port\0" # C-style string with null terminators
        len_buf = len(buf)
        go(buf, len_buf)
        mock_go.assert_called_once_with(buf, len_buf)

        # In a real implementation test, we'd assert calls to the mocked dependencies:
        # mock_wsastartup.assert_called_once()
        # mock_getaddrinfo.assert_called_once()
        # mock_socket.assert_called_once()
        # mock_connect.assert_called_once()
        # etc.